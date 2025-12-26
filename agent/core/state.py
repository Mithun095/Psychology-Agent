"""
Agent State Management for Cycology Agent.

Defines the state structure used by LangGraph for tracking
conversation context, mood, and crisis levels.
"""

from enum import Enum
from typing import TypedDict, Annotated, Optional, List
from datetime import datetime

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class MoodType(str, Enum):
    """Detected mood categories."""
    HAPPY = "happy"
    CONTENT = "content"
    NEUTRAL = "neutral"
    SAD = "sad"
    ANXIOUS = "anxious"
    ANGRY = "angry"
    CONFUSED = "confused"
    HOPEFUL = "hopeful"
    OVERWHELMED = "overwhelmed"
    LONELY = "lonely"


class CrisisLevel(str, Enum):
    """Crisis severity levels."""
    NONE = "none"           # Normal conversation
    LOW = "low"             # Mild distress, monitor
    MEDIUM = "medium"       # Significant distress, offer resources
    HIGH = "high"           # Serious concerns, strongly encourage help
    CRITICAL = "critical"   # Immediate danger, emergency response


class AgentState(TypedDict):
    """
    LangGraph agent state for mental health conversations.
    
    This state flows through all nodes in the agent graph,
    accumulating context and analysis as the conversation progresses.
    """
    # Conversation messages with automatic accumulation
    messages: Annotated[List[BaseMessage], add_messages]
    
    # Session tracking
    session_id: str
    user_id: Optional[str]
    
    # Mood analysis
    current_mood: MoodType
    mood_score: float  # -1.0 (very negative) to 1.0 (very positive)
    mood_trend: str    # "improving", "stable", "declining"
    
    # Crisis detection
    crisis_level: CrisisLevel
    crisis_keywords_found: List[str]
    
    # Escalation
    should_escalate: bool
    escalation_reason: Optional[str]
    
    # User context (persistent across sessions)
    user_context: dict
    
    # Response generation
    response_style: str  # "supportive", "grounding", "validating", "crisis"
    

def create_initial_state(session_id: str, user_id: Optional[str] = None) -> AgentState:
    """
    Create a fresh agent state for a new conversation.
    
    Args:
        session_id: Unique session identifier
        user_id: Optional user identifier for persistent context
        
    Returns:
        Initialized AgentState
    """
    return AgentState(
        messages=[],
        session_id=session_id,
        user_id=user_id,
        current_mood=MoodType.NEUTRAL,
        mood_score=0.0,
        mood_trend="stable",
        crisis_level=CrisisLevel.NONE,
        crisis_keywords_found=[],
        should_escalate=False,
        escalation_reason=None,
        user_context={
            "first_interaction": datetime.utcnow().isoformat(),
            "total_sessions": 1,
            "topics_discussed": [],
        },
        response_style="supportive",
    )
