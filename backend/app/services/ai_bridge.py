"""
AI Agent Bridge Service
Connects backend to AI agent for processing messages

Author: Vignesh (Backend Developer)
"""

import httpx
from typing import Optional, Dict, Any
from app.config import settings


async def send_message_to_agent(
    message: str,
    session_id: str,
    user_id: str,
    conversation_history: Optional[list] = None
) -> Dict[str, Any]:
    """
    Send user message to AI agent and get response
    
    Args:
        message: User's message
        session_id: Current chat session ID
        user_id: User ID
        conversation_history: Previous messages in conversation
    
    Returns:
        Dict with agent response and metadata
    """
    
    # Prepare request payload
    payload = {
        "message": message,
        "session_id": session_id,
        "user_id": user_id,
        "conversation_history": conversation_history or []
    }
    
    try:
        # Call AI agent API
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{settings.AGENT_URL}/api/chat",
                json=payload
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ AI Agent error: {response.status_code}")
                return {
                    "response": "I'm having trouble connecting right now. Please try again.",
                    "error": True
                }
    
    except httpx.TimeoutException:
        print("❌ AI Agent timeout")
        return {
            "response": "I'm taking a bit longer to respond. Please try again.",
            "error": True
        }
    
    except Exception as e:
        print(f"❌ AI Agent exception: {e}")
        return {
            "response": "I'm having trouble right now. Please try again shortly.",
            "error": True
        }


async def check_agent_health() -> bool:
    """Check if AI agent is running and healthy"""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{settings.AGENT_URL}/health")
            return response.status_code == 200
    except Exception:
        return False


