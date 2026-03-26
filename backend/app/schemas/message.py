"""
Message Pydantic Schemas
Request/Response validation schemas

Author: Vignesh (Backend Developer)
"""

from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


# Request Schemas
class MessageCreate(BaseModel):
    """Create message request"""
    session_id: str
    content: str = Field(..., min_length=1, max_length=5000)


class MessageSend(BaseModel):
    """Send message via WebSocket"""
    content: str = Field(..., min_length=1, max_length=5000)


# Response Schemas
class MessageResponse(BaseModel):
    """Message response"""
    id: str
    session_id: str
    sender_type: str  # "user" or "agent"
    content: str
    metadata: Optional[Dict[str, Any]] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class SessionCreate(BaseModel):
    """Create session request"""
    pass  # User ID comes from JWT token


class SessionResponse(BaseModel):
    """Session response"""
    id: str
    session_id: str
    user_id: str
    is_active: bool
    crisis_detected: bool
    escalated_to_professional: bool
    message_count: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ChatHistoryResponse(BaseModel):
    """Chat history response"""
    session: SessionResponse
    messages: list[MessageResponse]


