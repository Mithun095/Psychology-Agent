"""
Main LangGraph Agent for Cycology.

This is the core agent that orchestrates the mental health support
conversation, integrating mood analysis, crisis detection, and
empathetic response generation.
"""

from typing import Dict, Any, Optional, List
from enum import Enum
import uuid

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, BaseMessage
from langgraph.graph import StateGraph, END
from typing_extensions import TypedDict, Annotated
from langgraph.graph.message import add_messages


# ============================================================================
# LOCAL TYPE DEFINITIONS (avoiding circular imports)
# ============================================================================

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
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AgentState(TypedDict):
    """LangGraph agent state for mental health conversations."""
    messages: Annotated[List[BaseMessage], add_messages]
    session_id: str
    current_mood: MoodType
    mood_score: float
    crisis_level: CrisisLevel
    crisis_keywords_found: List[str]
    should_escalate: bool
    response_style: str


# ============================================================================
# IMPORT TOOLS (using sys.path workaround for direct execution)
# ============================================================================

import sys
import os

# Add parent directory to path for direct script execution
_current_dir = os.path.dirname(os.path.abspath(__file__))
_parent_dir = os.path.dirname(_current_dir)
if _parent_dir not in sys.path:
    sys.path.insert(0, _parent_dir)

from tools.crisis import detect_crisis, CrisisAssessment
from tools.mood import analyze_mood, MoodAssessment
from prompts.system import get_system_prompt, CRISIS_SYSTEM_PROMPT
from prompts.templates import format_crisis_resources, RESPONSE_TEMPLATES
from core.config import get_llm


# ============================================================================
# AGENT NODES
# ============================================================================

def analyze_mood_node(state: AgentState) -> Dict[str, Any]:
    """Analyze the mood from the latest user message."""
    messages = state.get("messages", [])
    
    if not messages:
        return {}
    
    # Get the latest user message
    latest_message = None
    for msg in reversed(messages):
        if isinstance(msg, HumanMessage):
            latest_message = msg.content
            break
    
    if not latest_message:
        return {}
    
    # Analyze mood
    assessment: MoodAssessment = analyze_mood(latest_message)
    
    # Map the mood type from tools module to local enum
    mood_map = {
        "happy": MoodType.HAPPY,
        "content": MoodType.CONTENT,
        "neutral": MoodType.NEUTRAL,
        "sad": MoodType.SAD,
        "anxious": MoodType.ANXIOUS,
        "angry": MoodType.ANGRY,
        "confused": MoodType.CONFUSED,
        "hopeful": MoodType.HOPEFUL,
        "overwhelmed": MoodType.OVERWHELMED,
        "lonely": MoodType.LONELY,
    }
    
    return {
        "current_mood": mood_map.get(assessment.mood.value, MoodType.NEUTRAL),
        "mood_score": assessment.score,
    }


def detect_crisis_node(state: AgentState) -> Dict[str, Any]:
    """Check the latest message for crisis indicators."""
    messages = state.get("messages", [])
    
    if not messages:
        return {}
    
    # Get the latest user message
    latest_message = None
    for msg in reversed(messages):
        if isinstance(msg, HumanMessage):
            latest_message = msg.content
            break
    
    if not latest_message:
        return {}
    
    # Detect crisis
    assessment: CrisisAssessment = detect_crisis(latest_message)
    
    # Map crisis level
    crisis_map = {
        "none": CrisisLevel.NONE,
        "low": CrisisLevel.LOW,
        "medium": CrisisLevel.MEDIUM,
        "high": CrisisLevel.HIGH,
        "critical": CrisisLevel.CRITICAL,
    }
    
    crisis_level = crisis_map.get(assessment.level.value, CrisisLevel.NONE)
    
    # Determine response style
    response_style = {
        CrisisLevel.CRITICAL: "crisis",
        CrisisLevel.HIGH: "crisis",
        CrisisLevel.MEDIUM: "resources",
        CrisisLevel.LOW: "supportive",
        CrisisLevel.NONE: "supportive",
    }.get(crisis_level, "supportive")
    
    return {
        "crisis_level": crisis_level,
        "crisis_keywords_found": assessment.keywords_found,
        "response_style": response_style,
    }


def check_escalation_node(state: AgentState) -> Dict[str, Any]:
    """Determine if the conversation should be escalated."""
    crisis_level = state.get("crisis_level", CrisisLevel.NONE)
    
    should_escalate = crisis_level in [CrisisLevel.CRITICAL, CrisisLevel.HIGH]
    
    return {
        "should_escalate": should_escalate,
    }


async def generate_response_node(state: AgentState) -> Dict[str, Any]:
    """Generate an empathetic response using the LLM."""
    messages = state.get("messages", [])
    current_mood = state.get("current_mood", MoodType.NEUTRAL)
    crisis_level = state.get("crisis_level", CrisisLevel.NONE)
    
    # Handle critical crisis with immediate intervention
    if crisis_level in [CrisisLevel.CRITICAL, CrisisLevel.HIGH]:
        crisis_resources = format_crisis_resources("india")
        crisis_response = RESPONSE_TEMPLATES["crisis_immediate"].format(
            crisis_resources=crisis_resources
        )
        return {
            "messages": [AIMessage(content=crisis_response)],
        }
    
    # Get appropriate system prompt
    from prompts.system import MoodType as PromptMoodType, CrisisLevel as PromptCrisisLevel
    
    # Map to prompt module's types
    prompt_mood = PromptMoodType(current_mood.value)
    prompt_crisis = PromptCrisisLevel(crisis_level.value)
    
    system_prompt = get_system_prompt(
        mood=prompt_mood,
        crisis_level=prompt_crisis,
    )
    
    # Build messages for LLM
    llm_messages = [SystemMessage(content=system_prompt)]
    
    # Add conversation history (limit to recent messages)
    recent_messages = messages[-10:] if len(messages) > 10 else messages
    llm_messages.extend(recent_messages)
    
    # Generate response with LLM
    try:
        llm = get_llm()
        response = await llm.ainvoke(llm_messages)
        response_content = response.content
    except Exception as e:
        # Fallback to a safe, empathetic default
        print(f"LLM Error: {e}")
        response_content = (
            "I hear you, and I'm here to listen. Sometimes just sharing "
            "what's on your mind can help. Would you like to tell me more "
            "about what you're experiencing?"
        )
    
    return {
        "messages": [AIMessage(content=response_content)],
    }


# ============================================================================
# GRAPH CONSTRUCTION
# ============================================================================

def create_agent() -> StateGraph:
    """Create the LangGraph agent for mental health support."""
    graph = StateGraph(AgentState)
    
    # Add nodes
    graph.add_node("analyze_mood", analyze_mood_node)
    graph.add_node("detect_crisis", detect_crisis_node)
    graph.add_node("check_escalation", check_escalation_node)
    graph.add_node("generate_response", generate_response_node)
    
    # Set entry point
    graph.set_entry_point("analyze_mood")
    
    # Add edges - sequential flow
    graph.add_edge("analyze_mood", "detect_crisis")
    graph.add_edge("detect_crisis", "check_escalation")
    graph.add_edge("check_escalation", "generate_response")
    graph.add_edge("generate_response", END)
    
    return graph.compile()


# ============================================================================
# HIGH-LEVEL API
# ============================================================================

_agent = None


def get_agent() -> StateGraph:
    """Get or create the agent instance."""
    global _agent
    if _agent is None:
        _agent = create_agent()
    return _agent


def create_initial_state(session_id: str) -> AgentState:
    """Create a fresh agent state for a new conversation."""
    return AgentState(
        messages=[],
        session_id=session_id,
        current_mood=MoodType.NEUTRAL,
        mood_score=0.0,
        crisis_level=CrisisLevel.NONE,
        crisis_keywords_found=[],
        should_escalate=False,
        response_style="supportive",
    )


async def run_agent(
    message: str,
    session_id: Optional[str] = None,
    existing_state: Optional[AgentState] = None,
) -> Dict[str, Any]:
    """Run the agent with a user message."""
    agent = get_agent()
    
    # Create or use existing state
    if existing_state:
        state = dict(existing_state)
    else:
        session_id = session_id or str(uuid.uuid4())
        state = create_initial_state(session_id)
    
    # Add the user message
    state["messages"] = list(state.get("messages", [])) + [HumanMessage(content=message)]
    
    # Run the agent
    result = await agent.ainvoke(state)
    
    # Extract response
    response_message = None
    for msg in reversed(result.get("messages", [])):
        if isinstance(msg, AIMessage):
            response_message = msg.content
            break
    
    return {
        "response": response_message or "I'm here to listen. How can I support you?",
        "session_id": result.get("session_id", session_id),
        "mood": result.get("current_mood", MoodType.NEUTRAL).value,
        "crisis_level": result.get("crisis_level", CrisisLevel.NONE).value,
        "should_escalate": result.get("should_escalate", False),
        "state": result,
    }
