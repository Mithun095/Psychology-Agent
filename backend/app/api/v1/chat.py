"""
Chat API Routes
WebSocket chat, session management, message history

Author: Vignesh (Backend Developer)
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException, status
from typing import List

from app.api.deps import get_current_user, security
from app.schemas.message import (
    SessionCreate,
    SessionResponse,
    MessageResponse,
    ChatHistoryResponse
)
from app.services.chat import (
    create_session,
    get_user_sessions,
    get_session,
    save_message,
    get_session_messages
)
from app.services.ai_bridge import send_message_to_agent
from app.utils.websocket import manager
from app.utils.security import decode_access_token


router = APIRouter()


@router.post("/sessions", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
async def create_new_session(
    session_data: SessionCreate,
    current_user: dict = Depends(get_current_user)
):
    """
    Create a new chat session
    
    Requires authentication
    """
    session = await create_session(current_user["id"])
    
    return SessionResponse(
        id=str(session.id),
        session_id=session.session_id,
        user_id=session.user_id,
        is_active=session.is_active,
        crisis_detected=session.crisis_detected,
        escalated_to_professional=session.escalated_to_professional,
        message_count=session.message_count,
        created_at=session.created_at,
        updated_at=session.updated_at
    )


@router.get("/sessions", response_model=List[SessionResponse])
async def get_my_sessions(
    current_user: dict = Depends(get_current_user),
    limit: int = 10
):
    """
    Get current user's chat sessions
    
    Returns list of sessions (most recent first)
    """
    sessions = await get_user_sessions(current_user["id"], limit)
    
    return [
        SessionResponse(
            id=session["id"],
            session_id=session["session_id"],
            user_id=session["user_id"],
            is_active=session["is_active"],
            crisis_detected=session.get("crisis_detected", False),
            escalated_to_professional=session.get("escalated_to_professional", False),
            message_count=session.get("message_count", 0),
            created_at=session["created_at"],
            updated_at=session["updated_at"]
        )
        for session in sessions
    ]


@router.get("/sessions/{session_id}/history", response_model=ChatHistoryResponse)
async def get_chat_history(
    session_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Get chat history for a session
    
    Returns session info and all messages
    """
    # Get session
    session = await get_session(session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    # Verify session belongs to user
    if session["user_id"] != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this session"
        )
    
    # Get messages
    messages = await get_session_messages(session_id)
    
    return ChatHistoryResponse(
        session=SessionResponse(
            id=session["id"],
            session_id=session["session_id"],
            user_id=session["user_id"],
            is_active=session["is_active"],
            crisis_detected=session.get("crisis_detected", False),
            escalated_to_professional=session.get("escalated_to_professional", False),
            message_count=session.get("message_count", 0),
            created_at=session["created_at"],
            updated_at=session["updated_at"]
        ),
        messages=[
            MessageResponse(
                id=msg["id"],
                session_id=msg["session_id"],
                sender_type=msg["sender_type"],
                content=msg["content"],
                metadata=msg.get("metadata"),
                created_at=msg["created_at"]
            )
            for msg in messages
        ]
    )


@router.websocket("/ws/{session_id}")
async def websocket_chat(websocket: WebSocket, session_id: str):
    """
    WebSocket endpoint for real-time chat
    
    Connect with: ws://localhost:8000/api/v1/chat/ws/{session_id}?token=your_jwt_token
    """
    
    # Get token from query params
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    
    # Verify token
    payload = decode_access_token(token)
    if not payload:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    
    user_id = payload.get("user_id")
    if not user_id:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    
    # Verify session belongs to user
    session = await get_session(session_id)
    if not session or session["user_id"] != user_id:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    
    # Accept connection
    await manager.connect(websocket, user_id)
    
    # Send welcome message
    await manager.send_personal_message(
        {
            "type": "connection",
            "message": "Connected to Cycology Agent",
            "session_id": session_id
        },
        user_id
    )
    
    try:
        while True:
            # Receive message from user
            data = await websocket.receive_json()
            user_message = data.get("content", "")
            
            if not user_message:
                continue
            
            # Save user message
            await save_message(session_id, "user", user_message)
            
            # Echo user message back
            await manager.send_personal_message(
                {
                    "type": "user_message",
                    "sender": "user",
                    "content": user_message,
                    "session_id": session_id
                },
                user_id
            )
            
            # Get conversation history
            messages = await get_session_messages(session_id, limit=10)
            conversation_history = [
                {"role": msg["sender_type"], "content": msg["content"]}
                for msg in messages[:-1]  # Exclude the just-sent message
            ]
            
            # Send to AI agent
            agent_response = await send_message_to_agent(
                message=user_message,
                session_id=session_id,
                user_id=user_id,
                conversation_history=conversation_history
            )
            
            # Save agent response
            agent_message = agent_response.get("response", "I'm having trouble responding right now.")
            await save_message(
                session_id,
                "agent",
                agent_message,
                metadata=agent_response.get("metadata")
            )
            
            # Send agent response to user
            await manager.send_personal_message(
                {
                    "type": "agent_message",
                    "sender": "agent",
                    "content": agent_message,
                    "session_id": session_id,
                    "metadata": agent_response.get("metadata")
                },
                user_id
            )
    
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)
        print(f"User {user_id} disconnected from session {session_id}")
    
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket, user_id)


@router.get("/test")
async def test_chat():
    """Test chat endpoint"""
    return {
        "message": "Chat API is working!",
        "endpoints": {
            "create_session": "/api/v1/chat/sessions (POST, requires auth)",
            "get_sessions": "/api/v1/chat/sessions (GET, requires auth)",
            "get_history": "/api/v1/chat/sessions/{session_id}/history (GET, requires auth)",
            "websocket": "ws://localhost:8000/api/v1/chat/ws/{session_id}?token=YOUR_JWT"
        }
    }


