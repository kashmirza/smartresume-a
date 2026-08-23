from fastapi import APIRouter, status
from pydantic import BaseModel, EmailStr

router = APIRouter(prefix="/auth", tags=["Authentication"])


class UserRegisterSchema(BaseModel):
    email: EmailStr
    password: str
    full_name: str


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegisterSchema):
    """
    Register a new user account.
    """
    return {
        "status": "success",
        "message": "User registered successfully",
        "data": {"email": user_data.email, "full_name": user_data.full_name}
    }


@router.post("/login")
async def login(login_data: UserLoginSchema):
    """
    Authenticate user and return JWT access token.
    """
    return {
        "status": "success",
        "access_token": "placeholder_jwt_token",
        "token_type": "bearer",
        "expires_in": 1440
    }


@router.get("/me")
async def get_current_user_profile():
    """
    Fetch authenticated user profile details.
    """
    return {
        "status": "success",
        "user": {
            "email": "user@example.com",
            "full_name": "Demo User",
            "is_active": True
        }
    }
