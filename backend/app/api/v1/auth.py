"""
Authentication API Routes
Register, login, anonymous user creation

Author: Vignesh (Backend Developer)
"""

from fastapi import APIRouter, HTTPException, status

from app.schemas.user import (
    UserRegister,
    UserLogin,
    AnonymousUserCreate,
    Token
)
from app.services.auth import (
    register_user,
    create_anonymous_user,
    login_user
)


router = APIRouter()


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister):
    """
    Register a new user
    
    - **username**: Unique username (3-50 characters)
    - **password**: Password (minimum 6 characters)
    - **email**: Optional email address
    - **is_anonymous**: Whether this is an anonymous account
    """
    return await register_user(user_data)


@router.post("/anonymous", response_model=Token, status_code=status.HTTP_201_CREATED)
async def create_anonymous(user_data: AnonymousUserCreate):
    """
    Create an anonymous user (no password required)
    
    Perfect for users who want to chat without registration
    
    - **display_name**: Optional display name (defaults to "Anonymous")
    """
    return await create_anonymous_user(user_data)


@router.post("/login", response_model=Token)
async def login(login_data: UserLogin):
    """
    Login with username and password
    
    - **username**: Your username
    - **password**: Your password
    
    Returns JWT access token
    """
    return await login_user(login_data)


@router.get("/test")
async def test_auth():
    """Test authentication endpoint"""
    return {
        "message": "Authentication API is working!",
        "endpoints": {
            "register": "/api/v1/auth/register",
            "login": "/api/v1/auth/login",
            "anonymous": "/api/v1/auth/anonymous"
        }
    }


