"""
Security and authentication utilities for SmartResume AI.

Provides password hashing and verification via Passlib (bcrypt), JWT access token creation
and decoding, OAuth2 scheme setup, and FastAPI current user dependency backed by MongoDB.
"""

from datetime import datetime, timedelta, timezone
import logging
import os
from typing import Any, Dict, Optional

from bson import ObjectId
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

logger = logging.getLogger(__name__)

# Password hashing context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Configuration from environment variables with production-grade defaults
SECRET_KEY = os.getenv("SECRET_KEY", "smartresume-ai-secret-key-change-in-production-2026")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# MongoDB Configuration for user lookup
MONGODB_URL = os.getenv("MONGODB_URL", os.getenv("MONGO_URI", "mongodb://localhost:27017"))
DATABASE_NAME = os.getenv("DATABASE_NAME", os.getenv("MONGO_DB", "smartresume_db"))

# OAuth2 password bearer scheme for FastAPI route security
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def hash_password(password: str) -> str:
    """Hash a plain text password using bcrypt.

    Args:
        password: Plain text password string to hash.

    Returns:
        Hashed password string.

    Raises:
        ValueError: If password is empty or not a string.
    """
    if not password or not isinstance(password, str):
        raise ValueError("Password must be a non-empty string.")
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain text password against a stored hash.

    Args:
        plain_password: Plain text password to check.
        hashed_password: Stored bcrypt hash string.

    Returns:
        True if the password matches the hash, False otherwise.
    """
    if not plain_password or not hashed_password:
        return False
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        logger.warning(f"Error verifying password hash: {e}")
        return False


def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """Create a signed JWT access token.

    Args:
        data: Dictionary of claims to encode into the token (e.g., {"sub": user_id}).
        expires_delta: Optional custom expiration timedelta. Defaults to ACCESS_TOKEN_EXPIRE_MINUTES.

    Returns:
        Encoded JWT token string.
    """
    to_encode = data.copy()
    now = datetime.now(timezone.utc)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({
        "exp": expire,
        "iat": now,
    })

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
    """FastAPI dependency to validate JWT bearer token and retrieve the user from MongoDB.

    Args:
        token: Bearer JWT token automatically extracted by OAuth2PasswordBearer.

    Returns:
        User document dictionary from MongoDB.

    Raises:
        HTTPException: 401 Unauthorized if token is invalid, expired, or user not found.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: Optional[str] = payload.get("sub") or payload.get("user_id") or payload.get("id")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = None
    try:
        # Attempt to retrieve existing database instance or initialize Motor client
        db = None
        try:
            from app.database import db as app_db  # type: ignore
            db = app_db
        except (ImportError, AttributeError):
            pass

        if db is None:
            try:
                from motor.motor_asyncio import AsyncIOMotorClient
                client = AsyncIOMotorClient(MONGODB_URL)
                db = client[DATABASE_NAME]
            except Exception as e:
                logger.error(f"MongoDB connection failure in get_current_user: {e}")
                raise credentials_exception

        # Construct query matching _id (as ObjectId or str), id, or email
        query_conditions = []
        if ObjectId.is_valid(user_id):
            query_conditions.append({"_id": ObjectId(user_id)})
        query_conditions.append({"_id": user_id})
        query_conditions.append({"id": user_id})
        query_conditions.append({"email": user_id})

        user = await db.users.find_one({"$or": query_conditions})

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Database lookup error in get_current_user: {e}")
        raise credentials_exception

    if user is None:
        raise credentials_exception

    # Convert BSON ObjectId to string for safe serialization
    if "_id" in user and isinstance(user["_id"], ObjectId):
        user["_id"] = str(user["_id"])

    return user
