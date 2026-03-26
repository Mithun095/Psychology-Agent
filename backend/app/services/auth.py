"""
Authentication Service
Handles user authentication, registration, and token management

Author: Vignesh (Backend Developer)
"""

from datetime import datetime
from typing import Optional
import uuid
from fastapi import HTTPException, status

from app.models.user import UserModel
from app.schemas.user import UserRegister, UserLogin, AnonymousUserCreate, UserResponse, Token
from app.utils.database import get_collection
from app.utils.security import verify_password, get_password_hash, create_access_token


async def register_user(user_data: UserRegister) -> Token:
    """Register a new user"""
    users_collection = get_collection("users")
    
    # Check if username already exists
    existing_user = await users_collection.find_one({"username": user_data.username})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Create new user
    new_user = UserModel(
        username=user_data.username,
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
        is_anonymous=user_data.is_anonymous,
        display_name=user_data.username if not user_data.is_anonymous else "Anonymous"
    )
    
    # Insert into database
    result = await users_collection.insert_one(new_user.model_dump(by_alias=True))
    user_id = str(result.inserted_id)
    
    # Create access token
    access_token = create_access_token(data={"user_id": user_id})
    
    # Return token with user info
    user_response = UserResponse(
        id=user_id,
        username=new_user.username,
        display_name=new_user.display_name,
        is_anonymous=new_user.is_anonymous,
        is_professional=new_user.is_professional,
        created_at=new_user.created_at
    )
    
    return Token(access_token=access_token, user=user_response)


async def create_anonymous_user(user_data: AnonymousUserCreate) -> Token:
    """Create anonymous user (no password required)"""
    users_collection = get_collection("users")
    
    # Generate unique username
    username = f"anon_{uuid.uuid4().hex[:12]}"
    
    # Create anonymous user with dummy password
    new_user = UserModel(
        username=username,
        hashed_password=get_password_hash(uuid.uuid4().hex),  # Random password they'll never need
        is_anonymous=True,
        display_name=user_data.display_name or "Anonymous"
    )
    
    # Insert into database
    result = await users_collection.insert_one(new_user.model_dump(by_alias=True))
    user_id = str(result.inserted_id)
    
    # Create access token
    access_token = create_access_token(data={"user_id": user_id})
    
    # Return token with user info
    user_response = UserResponse(
        id=user_id,
        username=new_user.username,
        display_name=new_user.display_name,
        is_anonymous=new_user.is_anonymous,
        is_professional=new_user.is_professional,
        created_at=new_user.created_at
    )
    
    return Token(access_token=access_token, user=user_response)


async def login_user(login_data: UserLogin) -> Token:
    """Login user with username and password"""
    users_collection = get_collection("users")
    
    # Find user by username
    user = await users_collection.find_one({"username": login_data.username})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    # Verify password
    if not verify_password(login_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    # Check if user is active
    if not user.get("is_active", True):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    # Update last active
    await users_collection.update_one(
        {"_id": user["_id"]},
        {"$set": {"last_active": datetime.utcnow()}}
    )
    
    # Create access token
    user_id = str(user["_id"])
    access_token = create_access_token(data={"user_id": user_id})
    
    # Return token with user info
    user_response = UserResponse(
        id=user_id,
        username=user["username"],
        display_name=user.get("display_name"),
        is_anonymous=user.get("is_anonymous", False),
        is_professional=user.get("is_professional", False),
        created_at=user["created_at"]
    )
    
    return Token(access_token=access_token, user=user_response)


async def get_user_by_id(user_id: str) -> Optional[dict]:
    """Get user by ID"""
    from bson import ObjectId
    users_collection = get_collection("users")
    
    try:
        user = await users_collection.find_one({"_id": ObjectId(user_id)})
        return user
    except Exception:
        return None


