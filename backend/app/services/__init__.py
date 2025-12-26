"""
Service Layer
Business logic for the application

Author: Vignesh (Backend Developer)
"""

from app.services.auth import (
    register_user,
    create_anonymous_user,
    login_user,
    get_user_by_id
)

from app.services.chat import (
    create_session,
    get_user_sessions,
    get_session,
    save_message,
    get_session_messages,
    mark_crisis_detected,
    mark_escalated,
    end_session
)

from app.services.ai_bridge import (
    send_message_to_agent,
    check_agent_health
)

__all__ = [
    # Auth services
    "register_user",
    "create_anonymous_user",
    "login_user",
    "get_user_by_id",
    # Chat services
    "create_session",
    "get_user_sessions",
    "get_session",
    "save_message",
    "get_session_messages",
    "mark_crisis_detected",
    "mark_escalated",
    "end_session",
    # AI Bridge
    "send_message_to_agent",
    "check_agent_health",
]


