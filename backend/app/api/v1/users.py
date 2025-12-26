"""
User Management API Routes
Get user profile, update profile

Author: Vignesh (Backend Developer)
"""

from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime

from app.api.deps import get_current_user
from app.schemas.user import UserProfile
from app.utils.database import get_collection


router = APIRouter()


@router.get("/me", response_model=UserProfile)
async def get_my_profile(current_user: dict = Depends(get_current_user)):
    """
    Get current user's profile
    
    Requires authentication (Bearer token)
    """
    return UserProfile(
        id=current_user["id"],
        username=current_user["username"],
        email=current_user.get("email"),
        display_name=current_user.get("display_name"),
        avatar_url=current_user.get("avatar_url"),
        is_anonymous=current_user.get("is_anonymous", False),
        is_professional=current_user.get("is_professional", False),
        is_active=current_user.get("is_active", True),
        created_at=current_user["created_at"],
        last_active=current_user.get("last_active", current_user["created_at"])
    )


@router.get("/{user_id}", response_model=UserProfile)
async def get_user_profile(
    user_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Get another user's profile
    
    Requires authentication
    """
    from bson import ObjectId
    users_collection = get_collection("users")
    
    try:
        user = await users_collection.find_one({"_id": ObjectId(user_id)})
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return UserProfile(
            id=str(user["_id"]),
            username=user["username"],
            email=user.get("email") if not user.get("is_anonymous") else None,
            display_name=user.get("display_name"),
            avatar_url=user.get("avatar_url"),
            is_anonymous=user.get("is_anonymous", False),
            is_professional=user.get("is_professional", False),
            is_active=user.get("is_active", True),
            created_at=user["created_at"],
            last_active=user.get("last_active", user["created_at"])
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid user ID: {str(e)}"
        )


@router.patch("/me")
async def update_my_profile(
    display_name: str = None,
    avatar_url: str = None,
    current_user: dict = Depends(get_current_user)
):
    """
    Update current user's profile
    
    Can update display_name and avatar_url
    """
    from bson import ObjectId
    users_collection = get_collection("users")
    
    update_data = {}
    if display_name is not None:
        update_data["display_name"] = display_name
    if avatar_url is not None:
        update_data["avatar_url"] = avatar_url
    
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No update data provided"
        )
    
    # Update user
    await users_collection.update_one(
        {"_id": ObjectId(current_user["id"])},
        {"$set": {**update_data, "last_active": datetime.utcnow()}}
    )
    
    return {"message": "Profile updated successfully", "updated": update_data}


@router.get("/test/public")
async def test_users():
    """Test users endpoint (no auth required)"""
    return {
        "message": "Users API is working!",
        "endpoints": {
            "my_profile": "/api/v1/users/me (requires auth)",
            "user_profile": "/api/v1/users/{user_id} (requires auth)",
            "update_profile": "/api/v1/users/me (PATCH, requires auth)"
        }
    }


