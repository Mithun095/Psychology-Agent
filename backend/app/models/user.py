"""
User Database Model
MongoDB user document structure

Author: Vignesh (Backend Developer)
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId


class PyObjectId(ObjectId):
    """Custom ObjectId type for Pydantic"""
    
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)
    
    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type="string")


class UserModel(BaseModel):
    """User database model"""
    
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    username: str = Field(..., min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    hashed_password: str
    is_anonymous: bool = False
    is_active: bool = True
    is_professional: bool = False  # True if psychologist/professional
    
    # Profile
    display_name: Optional[str] = None
    avatar_url: Optional[str] = None
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_active: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "username": "anonymous_user_123",
                "email": None,
                "is_anonymous": True,
                "display_name": "Anonymous"
            }
        }


