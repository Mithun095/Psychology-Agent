"""
Session Database Model
MongoDB chat session document structure

Author: Vignesh (Backend Developer)
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from bson import ObjectId
from app.models.user import PyObjectId


class SessionModel(BaseModel):
    """Chat session database model"""
    
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    session_id: str = Field(..., unique=True)  # Unique session identifier
    user_id: str  # References UserModel
    
    # Session status
    is_active: bool = True
    crisis_detected: bool = False
    escalated_to_professional: bool = False
    
    # Session metadata
    mood_history: list = Field(default_factory=list)  # Track mood changes
    message_count: int = 0
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    ended_at: Optional[datetime] = None
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "session_id": "session_123",
                "user_id": "user_456",
                "is_active": True,
                "crisis_detected": False,
                "message_count": 5
            }
        }


