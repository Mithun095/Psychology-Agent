"""
Chat Service
Handles chat sessions, messages, and conversation management

Author: Vignesh (Backend Developer)
"""

from datetime import datetime
from typing import List, Optional
import uuid

from app.models.session import SessionModel
from app.models.message import MessageModel
from app.utils.database import get_collection


async def create_session(user_id: str) -> SessionModel:
    """Create a new chat session"""
    sessions_collection = get_collection("sessions")
    
    # Generate unique session ID
    session_id = f"session_{uuid.uuid4().hex[:16]}"
    
    # Create new session
    new_session = SessionModel(
        session_id=session_id,
        user_id=user_id
    )
    
    # Insert into database
    await sessions_collection.insert_one(new_session.model_dump(by_alias=True))
    
    return new_session


async def get_user_sessions(user_id: str, limit: int = 10) -> List[dict]:
    """Get user's chat sessions"""
    sessions_collection = get_collection("sessions")
    
    cursor = sessions_collection.find(
        {"user_id": user_id}
    ).sort("created_at", -1).limit(limit)
    
    sessions = await cursor.to_list(length=limit)
    
    # Convert ObjectId to string
    for session in sessions:
        session["id"] = str(session["_id"])
        del session["_id"]
    
    return sessions


async def get_session(session_id: str) -> Optional[dict]:
    """Get session by ID"""
    sessions_collection = get_collection("sessions")
    
    session = await sessions_collection.find_one({"session_id": session_id})
    
    if session:
        session["id"] = str(session["_id"])
        del session["_id"]
    
    return session


async def save_message(
    session_id: str,
    sender_type: str,
    content: str,
    metadata: Optional[dict] = None
) -> MessageModel:
    """Save a message to the database"""
    messages_collection = get_collection("messages")
    sessions_collection = get_collection("sessions")
    
    # Create message
    new_message = MessageModel(
        session_id=session_id,
        sender_type=sender_type,
        content=content,
        metadata=metadata
    )
    
    # Insert into database
    await messages_collection.insert_one(new_message.model_dump(by_alias=True))
    
    # Update session message count and timestamp
    await sessions_collection.update_one(
        {"session_id": session_id},
        {
            "$inc": {"message_count": 1},
            "$set": {"updated_at": datetime.utcnow()}
        }
    )
    
    return new_message


async def get_session_messages(session_id: str, limit: int = 100) -> List[dict]:
    """Get messages for a session"""
    messages_collection = get_collection("messages")
    
    cursor = messages_collection.find(
        {"session_id": session_id}
    ).sort("created_at", 1).limit(limit)
    
    messages = await cursor.to_list(length=limit)
    
    # Convert ObjectId to string
    for message in messages:
        message["id"] = str(message["_id"])
        del message["_id"]
    
    return messages


async def mark_crisis_detected(session_id: str):
    """Mark session as having crisis detected"""
    sessions_collection = get_collection("sessions")
    
    await sessions_collection.update_one(
        {"session_id": session_id},
        {"$set": {"crisis_detected": True, "updated_at": datetime.utcnow()}}
    )


async def mark_escalated(session_id: str):
    """Mark session as escalated to professional"""
    sessions_collection = get_collection("sessions")
    
    await sessions_collection.update_one(
        {"session_id": session_id},
        {
            "$set": {
                "escalated_to_professional": True,
                "updated_at": datetime.utcnow()
            }
        }
    )


async def end_session(session_id: str):
    """End a chat session"""
    sessions_collection = get_collection("sessions")
    
    await sessions_collection.update_one(
        {"session_id": session_id},
        {
            "$set": {
                "is_active": False,
                "ended_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
        }
    )


