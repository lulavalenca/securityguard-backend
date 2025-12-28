"""User schemas."""

from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
from app.models.user import UserRole


class UserBase(BaseModel):
    """User base schema."""
    username: str = Field(..., min_length=3, max_length=255)
    email: EmailStr
    full_name: Optional[str] = Field(None, max_length=255)
    role: UserRole = UserRole.VIEWER


class UserCreate(UserBase):
    """User creation schema."""
    password: str = Field(..., min_length=8, max_length=255)


class UserLogin(BaseModel):
    """User login schema."""
    username: str = Field(..., min_length=3, max_length=255)
    password: str = Field(..., min_length=8, max_length=255)


class UserUpdate(BaseModel):
    """User update schema."""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, max_length=255)
    role: Optional[UserRole] = None
    password: Optional[str] = Field(None, min_length=8, max_length=255)


class UserResponse(UserBase):
    """User response schema."""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """Token response schema."""
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"
    expires_in: int
