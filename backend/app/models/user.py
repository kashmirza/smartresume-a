"""
User model for SmartResume AI.
"""

from datetime import datetime
from enum import Enum
from typing import Optional
import uuid

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CareerLevel(str, Enum):
    """Career experience levels for users."""
    STUDENT = "Student"
    FRESH_GRADUATE = "Fresh Graduate"
    JUNIOR = "Junior"
    MID_LEVEL = "Mid-Level"
    EXPERIENCED = "Experienced"


class User(BaseModel):
    """
    User domain and database model.
    """
    user_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique identifier for the user"
    )
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Full name of the user"
    )
    email: EmailStr = Field(
        ...,
        description="Unique email address"
    )
    password_hash: str = Field(
        ...,
        description="Hashed password string"
    )
    career_level: CareerLevel = Field(
        default=CareerLevel.FRESH_GRADUATE,
        description="User's current career level"
    )
    target_role: Optional[str] = Field(
        default=None,
        description="Desired or target job position"
    )
    is_active: bool = Field(
        default=True,
        description="Indicates whether the user account is active"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when the user account was created"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when the user account was last updated"
    )

    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,
        json_schema_extra={
            "example": {
                "user_id": "a1b2c3d4-e5f6-7890-abcd-1234567890ab",
                "name": "Alex Johnson",
                "email": "alex.johnson@example.com",
                "password_hash": "$2b$12$eImiTXuWVxfM37uY4JANjO5E.5218d6a789abcdef",
                "career_level": "Fresh Graduate",
                "target_role": "Full Stack Developer",
                "is_active": True,
                "created_at": "2026-08-22T12:00:00Z",
                "updated_at": "2026-08-22T12:00:00Z"
            }
        }
    )
