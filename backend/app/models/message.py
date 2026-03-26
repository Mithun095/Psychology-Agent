"""
Message Database Model
MongoDB message document structure

Author: Vignesh (Backend Developer)
"""

from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from bson import ObjectId
from app.models.user import PyObjectId


class MessageModel(BaseModel):
    """Chat message database model"""
    
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    session_id: str  # References SessionModel
    sender_type: str  # "user" or "agent"
    content: str
    
    # Metadata
    metadata: Optional[Dict[str, Any]] = None  # Extra data (sentiment, crisis_detected, etc.)
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "session_id": "session_123",
                "sender_type": "user",
                "content": "I'm feeling really down today...",
                "metadata": {"sentiment": "negative"}
            }
        }


