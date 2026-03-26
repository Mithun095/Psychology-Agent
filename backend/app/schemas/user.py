"""
User Pydantic Schemas
Request/Response validation schemas

Author: Vignesh (Backend Developer)
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


# Request Schemas
class UserRegister(BaseModel):
    """User registration request"""
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
    email: Optional[EmailStr] = None
    is_anonymous: bool = False


class UserLogin(BaseModel):
    """User login request"""
    username: str
    password: str


class AnonymousUserCreate(BaseModel):
    """Anonymous user creation request"""
    display_name: Optional[str] = "Anonymous"


# Response Schemas
class UserResponse(BaseModel):
    """User response (public data)"""
    id: str
    username: str
    display_name: Optional[str] = None
    is_anonymous: bool
    is_professional: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserProfile(BaseModel):
    """User profile (detailed)"""
    id: str
    username: str
    email: Optional[EmailStr] = None
    display_name: Optional[str] = None
    avatar_url: Optional[str] = None
    is_anonymous: bool
    is_professional: bool
    is_active: bool
    created_at: datetime
    last_active: datetime
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    """JWT Token response"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class TokenData(BaseModel):
    """Token payload data"""
    user_id: Optional[str] = None


