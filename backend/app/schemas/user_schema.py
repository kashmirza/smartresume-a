"""
User schemas for API requests and responses.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator, model_validator

from ..models.user import CareerLevel


class UserCreate(BaseModel):
    """Payload schema for user registration."""
    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Full name of the user",
        examples=["Alex Johnson"]
    )
    email: EmailStr = Field(
        ...,
        description="Valid email address for registration",
        examples=["alex.johnson@example.com"]
    )
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="Plain text user password (minimum 8 characters)",
        examples=["SecurePass123!"]
    )
    career_level: Optional[CareerLevel] = Field(
        default=CareerLevel.FRESH_GRADUATE,
        description="User's current career level"
    )
    target_role: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Desired or target job title",
        examples=["Full Stack Developer"]
    )

    @field_validator("password")
    @classmethod
    def validate_password_complexity(cls, value: str) -> str:
        """Ensure password meets minimum length requirement."""
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        return value


class UserLogin(BaseModel):
    """Payload schema for user authentication."""
    email: EmailStr = Field(
        ...,
        description="Registered user email",
        examples=["alex.johnson@example.com"]
    )
    password: str = Field(
        ...,
        min_length=1,
        description="User password",
        examples=["SecurePass123!"]
    )


class UserUpdate(BaseModel):
    """Payload schema for updating user details."""
    name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=100,
        description="Updated full name"
    )
    email: Optional[EmailStr] = Field(
        default=None,
        description="Updated email address"
    )
    password: Optional[str] = Field(
        default=None,
        min_length=8,
        max_length=128,
        description="Updated password (optional)"
    )
    career_level: Optional[CareerLevel] = Field(
        default=None,
        description="Updated career experience level"
    )
    target_role: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Updated target role"
    )

    @model_validator(mode="after")
    def check_at_least_one_field(self) -> "UserUpdate":
        """Verify that at least one attribute is provided for update."""
        fields_set = self.model_fields_set
        if not fields_set:
            raise ValueError("At least one field must be provided for update.")
        return self


class UserResponse(BaseModel):
    """Response schema representing a user profile."""
    user_id: str = Field(..., description="Unique user identifier")
    name: str = Field(..., description="User's full name")
    email: EmailStr = Field(..., description="User's email address")
    career_level: CareerLevel = Field(..., description="User's career level")
    target_role: Optional[str] = Field(default=None, description="Target job title")
    is_active: bool = Field(default=True, description="Account active status")
    created_at: datetime = Field(..., description="Account creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True
    )
