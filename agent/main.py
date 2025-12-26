"""
Cycology AI Agent - FastAPI Entry Point.

Exposes the mental health support agent via REST API endpoints.
"""

import sys
import os

# Add current directory to path for module imports
_current_dir = os.path.dirname(os.path.abspath(__file__))
if _current_dir not in sys.path:
    sys.path.insert(0, _current_dir)

import uuid
from typing import Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from core.agent import run_agent, get_agent, create_initial_state, MoodType, CrisisLevel
from core.config import settings, get_available_providers


# ============================================================================
# LIFESPAN & SETUP
# ============================================================================

# In-memory session store
sessions: dict = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    # Startup
    print("🧠 Cycology Agent Starting...")
    
    # Check available LLM providers
    try:
        providers = get_available_providers()
        if providers:
            print(f"✓ Available LLM providers: {[p.value for p in providers]}")
        else:
            print("⚠ No LLM providers available. Please configure Ollama, Groq, or Gemini.")
    except Exception as e:
        print(f"⚠ Could not check providers: {e}")
    
    # Warm up the agent
    try:
        get_agent()
        print("✓ Agent initialized")
    except Exception as e:
        print(f"⚠ Agent initialization warning: {e}")
    
    print("✓ Server ready at http://localhost:8001")
    print("  Try: POST /chat with {\"message\": \"Hello\"}")
    
    yield
    
    # Shutdown
    print("👋 Cycology Agent shutting down...")


# ============================================================================
# FASTAPI APP
# ============================================================================

app = FastAPI(
    title="Cycology AI Agent",
    description="Empathetic mental health support chatbot powered by LangGraph",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str = Field(..., min_length=1, max_length=5000, description="User message")
    session_id: Optional[str] = Field(None, description="Session ID for conversation continuity")


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    response: str = Field(..., description="Agent's response")
    session_id: str = Field(..., description="Session ID for this conversation")
    mood: str = Field(..., description="Detected mood")
    crisis_level: str = Field(..., description="Detected crisis level")
    should_escalate: bool = Field(..., description="Whether professional escalation is recommended")


class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str
    environment: str
    available_providers: list


class SessionInfo(BaseModel):
    """Response model for session info."""
    session_id: str
    turn_count: int


# ============================================================================
# ENDPOINTS
# ============================================================================

@app.get("/health", response_model=HealthResponse, tags=["System"])
async def health_check():
    """Health check endpoint."""
    try:
        providers = get_available_providers()
        provider_list = [p.value for p in providers]
    except Exception:
        provider_list = []
    
    return HealthResponse(
        status="healthy",
        environment=settings.environment,
        available_providers=provider_list,
    )


@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat(request: ChatRequest):
    """
    Send a message and receive an empathetic response.
    
    The agent will:
    1. Analyze the emotional content of your message
    2. Check for crisis indicators  
    3. Generate a supportive, empathetic response
    """
    try:
        # Get or create session state
        session_id = request.session_id or str(uuid.uuid4())
        existing_state = sessions.get(session_id)
        
        # Run the agent
        result = await run_agent(
            message=request.message,
            session_id=session_id,
            existing_state=existing_state,
        )
        
        # Store updated state
        sessions[session_id] = result["state"]
        
        return ChatResponse(
            response=result["response"],
            session_id=session_id,
            mood=result["mood"],
            crisis_level=result["crisis_level"],
            should_escalate=result["should_escalate"],
        )
        
    except Exception as e:
        print(f"Error in chat: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"I'm having trouble responding right now: {str(e)}"
        )


@app.get("/session/{session_id}", response_model=SessionInfo, tags=["Session"])
async def get_session(session_id: str):
    """Get information about a conversation session."""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    state = sessions[session_id]
    messages = state.get("messages", [])
    
    return SessionInfo(
        session_id=session_id,
        turn_count=len(messages) // 2,
    )


@app.delete("/session/{session_id}", tags=["Session"])
async def end_session(session_id: str):
    """End and clear a conversation session."""
    if session_id in sessions:
        del sessions[session_id]
        return {"message": "Session ended", "session_id": session_id}
    
    raise HTTPException(status_code=404, detail="Session not found")


@app.get("/", tags=["System"])
async def root():
    """Root endpoint with basic info."""
    return {
        "name": "Cycology AI Agent",
        "version": "0.1.0",
        "description": "Empathetic mental health support companion",
        "docs": "/docs",
        "endpoints": {
            "chat": "POST /chat - Send a message",
            "health": "GET /health - Check service health",
        }
    }


# ============================================================================
# RUN
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
    )
