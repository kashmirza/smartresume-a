"""
Authentication routes for SmartResume AI.

Handles user registration, login, profile retrieval, profile updates, and password changes.
"""

from datetime import datetime, timezone
import logging
from typing import Any, Dict

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status

from app.config.database import get_collection
from app.utils.security import (
    create_access_token,
    get_current_user,
    hash_password,
    verify_password,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(body: Dict[str, Any]):
    """
    Register a new user account with email and password.
    """
    email = (body.get("email") or "").strip().lower()
    password = body.get("password") or ""
    full_name = body.get("full_name") or body.get("fullName") or body.get("name") or ""
    career_level = body.get("career_level") or body.get("careerLevel") or ""
    target_role = body.get("target_role") or body.get("targetRole") or ""

    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is required"
        )
    if not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password is required"
        )

    users_col = get_collection("users")
    existing_user = await users_col.find_one({"email": email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered"
        )

    hashed_pw = hash_password(password)
    now = datetime.now(timezone.utc).isoformat()

    user_doc = {
        "email": email,
        "password": hashed_pw,
        "full_name": full_name,
        "career_level": career_level,
        "target_role": target_role,
        "created_at": now,
        "updated_at": now,
    }

    result = await users_col.insert_one(user_doc)
    user_id = str(result.inserted_id)

    access_token = create_access_token({"sub": user_id, "email": email})

    return {
        "status": "success",
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user_id,
            "email": email,
            "full_name": full_name,
            "career_level": career_level,
            "target_role": target_role,
        }
    }


@router.post("/login")
async def login(body: Dict[str, Any]):
    """
    Authenticate user with email and password and return a JWT access token.
    """
    email = (body.get("email") or "").strip().lower()
    password = body.get("password") or ""

    if not email or not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email and password are required"
        )

    users_col = get_collection("users")
    user = await users_col.find_one({"email": email})

    if not user or not verify_password(password, user.get("password", "")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = str(user["_id"])
    full_name = user.get("full_name") or user.get("fullName") or ""
    career_level = user.get("career_level") or user.get("careerLevel") or ""
    target_role = user.get("target_role") or user.get("targetRole") or ""

    access_token = create_access_token({"sub": user_id, "email": email})

    return {
        "status": "success",
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user_id,
            "email": email,
            "full_name": full_name,
            "career_level": career_level,
            "target_role": target_role,
        }
    }


@router.get("/me")
async def get_me(current_user: Dict[str, Any] = Depends(get_current_user)):
    """
    Get profile information for the currently authenticated user.
    """
    user_id = str(current_user.get("id") or current_user.get("_id"))
    full_name = current_user.get("full_name") or current_user.get("fullName") or ""
    
    return {
        "status": "success",
        "user": {
            "id": user_id,
            "email": current_user.get("email"),
            "full_name": full_name,
            "career_level": current_user.get("career_level") or current_user.get("careerLevel") or "",
            "target_role": current_user.get("target_role") or current_user.get("targetRole") or "",
            "created_at": current_user.get("created_at"),
        }
    }


@router.put("/profile")
async def update_profile(
    body: Dict[str, Any],
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    """
    Update profile details for the authenticated user.
    """
    user_id = str(current_user.get("id") or current_user.get("_id"))
    users_col = get_collection("users")

    update_fields = {}
    if "full_name" in body:
        update_fields["full_name"] = body["full_name"]
    elif "fullName" in body:
        update_fields["full_name"] = body["fullName"]

    if "career_level" in body:
        update_fields["career_level"] = body["career_level"]
    elif "careerLevel" in body:
        update_fields["career_level"] = body["careerLevel"]

    if "target_role" in body:
        update_fields["target_role"] = body["target_role"]
    elif "targetRole" in body:
        update_fields["target_role"] = body["targetRole"]

    update_fields["updated_at"] = datetime.now(timezone.utc).isoformat()

    query = {"_id": ObjectId(user_id)} if ObjectId.is_valid(user_id) else {"_id": user_id}
    await users_col.update_one(query, {"$set": update_fields})

    updated_user = await users_col.find_one(query)
    if not updated_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    full_name = updated_user.get("full_name") or updated_user.get("fullName") or ""

    return {
        "status": "success",
        "user": {
            "id": user_id,
            "email": updated_user.get("email"),
            "full_name": full_name,
            "career_level": updated_user.get("career_level") or updated_user.get("careerLevel") or "",
            "target_role": updated_user.get("target_role") or updated_user.get("targetRole") or "",
        }
    }


@router.put("/change-password")
async def change_password(
    body: Dict[str, Any],
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    """
    Change password for the authenticated user.
    """
    current_pw = body.get("current_password") or body.get("currentPassword") or body.get("old_password") or ""
    new_pw = body.get("new_password") or body.get("newPassword") or ""

    if not current_pw or not new_pw:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password and new password are required"
        )

    user_id = str(current_user.get("id") or current_user.get("_id"))
    users_col = get_collection("users")
    query = {"_id": ObjectId(user_id)} if ObjectId.is_valid(user_id) else {"_id": user_id}

    user = await users_col.find_one(query)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if not verify_password(current_pw, user.get("password", "")):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect current password"
        )

    hashed_new_pw = hash_password(new_pw)
    now = datetime.now(timezone.utc).isoformat()

    await users_col.update_one(
        query,
        {"$set": {"password": hashed_new_pw, "updated_at": now}}
    )

    return {
        "status": "success",
        "message": "Password updated successfully"
    }
