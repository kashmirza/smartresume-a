"""
Security and authentication utilities for SmartResume AI.

Provides password hashing and verification via Passlib (bcrypt), JWT access token creation
and decoding, and FastAPI current user dependency backed by MongoDB.
"""

from datetime import datetime, timedelta, timezone
import logging
from typing import Any, Dict, Optional

import bcrypt as _bcrypt
from bson import ObjectId
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.config.settings import settings
from app.config.database import get_collection

logger = logging.getLogger(__name__)

# OAuth2 scheme for swagger UI and standard bearer auth
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)


def hash_password(password: str) -> str:
    """Hash a plain text password using bcrypt directly (passlib-compatible format)."""
    if not password or not isinstance(password, str):
        raise ValueError("Password must be a non-empty string.")
    # bcrypt only accepts passwords up to 72 bytes
    password_bytes = password.encode("utf-8")[:72]
    salt = _bcrypt.gensalt(rounds=12)
    hashed = _bcrypt.hashpw(password_bytes, salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain text password against a stored bcrypt hash."""
    if not plain_password or not hashed_password:
        return False
    try:
        password_bytes = plain_password.encode("utf-8")[:72]
        hashed_bytes = hashed_password.encode("utf-8")
        return _bcrypt.checkpw(password_bytes, hashed_bytes)
    except Exception as e:
        logger.warning(f"Error verifying password hash: {e}")
        return False


def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """Create a signed JWT access token."""
    to_encode = data.copy()
    now = datetime.now(timezone.utc)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)

    to_encode.update({
        "exp": expire,
        "iat": now,
    })

    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    """Decode and validate a JWT access token."""
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except JWTError as e:
        logger.warning(f"JWT decode error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(
    request: Request,
    token: Optional[str] = Depends(oauth2_scheme),
) -> Dict[str, Any]:
    """FastAPI dependency to validate JWT bearer token and retrieve current user from MongoDB."""
    # Fallback to Authorization header if OAuth2PasswordBearer did not catch token
    if not token:
        auth_header = request.headers.get("Authorization") or request.headers.get("authorization")
        if auth_header:
            if auth_header.lower().startswith("bearer "):
                token = auth_header.split(" ", 1)[1].strip()
            else:
                token = auth_header.strip()

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = decode_access_token(token)
    user_id: Optional[str] = payload.get("sub") or payload.get("user_id") or payload.get("id")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )

    users_collection = get_collection("users")

    query_conditions = []
    if ObjectId.is_valid(user_id):
        query_conditions.append({"_id": ObjectId(user_id)})
    query_conditions.append({"_id": user_id})
    query_conditions.append({"id": user_id})
    query_conditions.append({"email": user_id})

    user = await users_collection.find_one({"$or": query_conditions})

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if "_id" in user:
        user["id"] = str(user["_id"])
        user["_id"] = str(user["_id"])

    return user
