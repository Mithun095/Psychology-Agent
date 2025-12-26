"""
Main LangGraph Agent for Cycology.

This is the core agent that orchestrates the mental health support
conversation, integrating mood analysis, crisis detection, and
empathetic response generation.
"""

from typing import Dict, Any, Optional
import uuid

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, END

from .state import AgentState, create_initial_state, MoodType, CrisisLevel
from .config import get_llm
from ..prompts.system import get_system_prompt, CRISIS_SYSTEM_PROMPT
from ..prompts.templates import (
    format_crisis_resources,
    EMPATHY_RESPONSES,
    GROUNDING_EXERCISES,
    RESPONSE_TEMPLATES,
)
from ..tools.crisis import detect_crisis, CrisisAssessment
from ..tools.mood import analyze_mood, MoodAssessment
from ..tools.escalation import should_escalate


# ============================================================================
# AGENT NODES
# ============================================================================

def analyze_mood_node(state: AgentState) -> Dict[str, Any]:
    """
    Analyze the mood from the latest user message.
    
    This node runs mood detection on the incoming message and
    updates the state with mood information.
    """
    messages = state.get("messages", [])
    
    if not messages:
        return state
    
    # Get the latest user message
    latest_message = None
    for msg in reversed(messages):
        if isinstance(msg, HumanMessage):
            latest_message = msg.content
            break
    
    if not latest_message:
        return state
    
    # Analyze mood
    assessment: MoodAssessment = analyze_mood(latest_message)
    
    return {
        "current_mood": assessment.mood,
        "mood_score": assessment.score,
    }


def detect_crisis_node(state: AgentState) -> Dict[str, Any]:
    """
    Check the latest message for crisis indicators.
    
    This is a critical safety node that identifies users
    who may be at risk and adjusts the response strategy.
    """
    messages = state.get("messages", [])
    
    if not messages:
        return state
    
    # Get the latest user message
    latest_message = None
    for msg in reversed(messages):
        if isinstance(msg, HumanMessage):
            latest_message = msg.content
            break
    
    if not latest_message:
        return state
    
    # Detect crisis
    assessment: CrisisAssessment = detect_crisis(latest_message)
    
    # Determine response style based on crisis level
    response_style = {
        CrisisLevel.CRITICAL: "crisis",
        CrisisLevel.HIGH: "crisis",
        CrisisLevel.MEDIUM: "resources",
        CrisisLevel.LOW: "supportive",
        CrisisLevel.NONE: "supportive",
    }.get(assessment.level, "supportive")
    
    return {
        "crisis_level": assessment.level,
        "crisis_keywords_found": assessment.keywords_found,
        "response_style": response_style,
    }


def check_escalation_node(state: AgentState) -> Dict[str, Any]:
    """
    Determine if the conversation should be escalated to professional support.
    """
    crisis_level = state.get("crisis_level", CrisisLevel.NONE)
    current_mood = state.get("current_mood", MoodType.NEUTRAL)
    mood_trend = state.get("mood_trend", "stable")
    messages = state.get("messages", [])
    
    # Count conversation turns
    turn_count = sum(1 for m in messages if isinstance(m, HumanMessage))
    
    decision = should_escalate(
        crisis_level=crisis_level,
        current_mood=current_mood,
        mood_trend=mood_trend,
        conversation_turns=turn_count,
    )
    
    return {
        "should_escalate": decision.should_escalate,
        "escalation_reason": decision.reason,
    }


async def generate_response_node(state: AgentState) -> Dict[str, Any]:
    """
    Generate an empathetic response using the LLM.
    
    This node creates the actual response to the user, taking into
    account mood, crisis level, and conversation context.
    """
    messages = state.get("messages", [])
    current_mood = state.get("current_mood", MoodType.NEUTRAL)
    crisis_level = state.get("crisis_level", CrisisLevel.NONE)
    response_style = state.get("response_style", "supportive")
    
    # Get appropriate system prompt
    system_prompt = get_system_prompt(
        mood=current_mood,
        crisis_level=crisis_level,
    )
    
    # Handle critical crisis with immediate intervention
    if crisis_level in [CrisisLevel.CRITICAL, CrisisLevel.HIGH]:
        crisis_resources = format_crisis_resources("india")
        crisis_response = RESPONSE_TEMPLATES["crisis_immediate"].format(
            crisis_resources=crisis_resources
        )
        
        return {
            "messages": [AIMessage(content=crisis_response)],
        }
    
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
        response_content = (
            "I hear you, and I'm here to listen. Sometimes just sharing "
            "what's on your mind can help. Would you like to tell me more "
            "about what you're experiencing?"
        )
    
    return {
        "messages": [AIMessage(content=response_content)],
    }


# ============================================================================
# ROUTING FUNCTIONS
# ============================================================================

def should_respond_crisis(state: AgentState) -> str:
    """Route based on crisis level."""
    crisis_level = state.get("crisis_level", CrisisLevel.NONE)
    
    if crisis_level in [CrisisLevel.CRITICAL, CrisisLevel.HIGH]:
        return "crisis_response"
    return "normal_response"


# ============================================================================
# GRAPH CONSTRUCTION
# ============================================================================

def create_agent() -> StateGraph:
    """
    Create the LangGraph agent for mental health support.
    
    Graph flow:
    1. Analyze mood from user message
    2. Detect crisis indicators
    3. Check escalation needs
    4. Generate empathetic response
    
    Returns:
        Compiled StateGraph
    """
    # Create the graph
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

# Cached agent instance
_agent = None


def get_agent() -> StateGraph:
    """Get or create the agent instance."""
    global _agent
    if _agent is None:
        _agent = create_agent()
    return _agent


async def run_agent(
    message: str,
    session_id: Optional[str] = None,
    existing_state: Optional[AgentState] = None,
) -> Dict[str, Any]:
    """
    Run the agent with a user message.
    
    Args:
        message: User's message
        session_id: Session identifier (generated if not provided)
        existing_state: Existing state to continue from
        
    Returns:
        Dictionary with response and updated state information
    """
    agent = get_agent()
    
    # Create or use existing state
    if existing_state:
        state = existing_state
    else:
        session_id = session_id or str(uuid.uuid4())
        state = create_initial_state(session_id)
    
    # Add the user message
    state["messages"].append(HumanMessage(content=message))
    
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
        "session_id": result.get("session_id"),
        "mood": result.get("current_mood", MoodType.NEUTRAL).value,
        "crisis_level": result.get("crisis_level", CrisisLevel.NONE).value,
        "should_escalate": result.get("should_escalate", False),
        "state": result,
    }
