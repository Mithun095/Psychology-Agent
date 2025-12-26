"""
Conversation Memory for Cycology Agent.

Provides persistent storage for conversation history using Redis,
with automatic summarization for long conversations.
"""

import json
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage


@dataclass
class ConversationTurn:
    """A single turn in the conversation."""
    role: str  # "user" or "assistant"
    content: str
    timestamp: str
    mood: Optional[str] = None
    crisis_level: Optional[str] = None


@dataclass
class ConversationSession:
    """Complete conversation session data."""
    session_id: str
    user_id: Optional[str]
    turns: List[ConversationTurn]
    created_at: str
    updated_at: str
    summary: Optional[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class MemoryStore:
    """
    Abstract base for memory storage backends.
    
    Provides a simple interface that can be implemented
    with Redis, in-memory, or other storage solutions.
    """
    
    async def save(self, session_id: str, data: dict) -> None:
        """Save session data."""
        raise NotImplementedError
    
    async def load(self, session_id: str) -> Optional[dict]:
        """Load session data."""
        raise NotImplementedError
    
    async def delete(self, session_id: str) -> None:
        """Delete session data."""
        raise NotImplementedError
    
    async def exists(self, session_id: str) -> bool:
        """Check if session exists."""
        raise NotImplementedError


class InMemoryStore(MemoryStore):
    """Simple in-memory storage for development."""
    
    def __init__(self):
        self._store: Dict[str, dict] = {}
    
    async def save(self, session_id: str, data: dict) -> None:
        self._store[session_id] = data
    
    async def load(self, session_id: str) -> Optional[dict]:
        return self._store.get(session_id)
    
    async def delete(self, session_id: str) -> None:
        self._store.pop(session_id, None)
    
    async def exists(self, session_id: str) -> bool:
        return session_id in self._store


class RedisStore(MemoryStore):
    """Redis-based storage for production."""
    
    def __init__(self, redis_url: str, ttl_hours: int = 24):
        self._redis_url = redis_url
        self._ttl_seconds = ttl_hours * 3600
        self._client = None
    
    async def _get_client(self):
        """Lazy initialization of Redis client."""
        if self._client is None:
            try:
                import redis.asyncio as redis
                self._client = redis.from_url(self._redis_url)
            except ImportError:
                raise RuntimeError("redis package required for RedisStore")
        return self._client
    
    async def save(self, session_id: str, data: dict) -> None:
        client = await self._get_client()
        key = f"cycology:session:{session_id}"
        await client.setex(key, self._ttl_seconds, json.dumps(data))
    
    async def load(self, session_id: str) -> Optional[dict]:
        client = await self._get_client()
        key = f"cycology:session:{session_id}"
        data = await client.get(key)
        if data:
            return json.loads(data)
        return None
    
    async def delete(self, session_id: str) -> None:
        client = await self._get_client()
        key = f"cycology:session:{session_id}"
        await client.delete(key)
    
    async def exists(self, session_id: str) -> bool:
        client = await self._get_client()
        key = f"cycology:session:{session_id}"
        return await client.exists(key) > 0


class ConversationMemory:
    """
    Manages conversation memory with persistence.
    
    Features:
    - Store full conversation history
    - Automatic summarization for long conversations
    - Session-based retrieval
    - Context persistence across sessions
    """
    
    def __init__(
        self,
        store: Optional[MemoryStore] = None,
        max_turns_before_summary: int = 20,
    ):
        """
        Initialize conversation memory.
        
        Args:
            store: Storage backend (defaults to in-memory)
            max_turns_before_summary: Trigger summarization after this many turns
        """
        self._store = store or InMemoryStore()
        self._max_turns = max_turns_before_summary
        self._sessions: Dict[str, ConversationSession] = {}
    
    async def get_or_create_session(
        self,
        session_id: str,
        user_id: Optional[str] = None,
    ) -> ConversationSession:
        """
        Get existing session or create new one.
        
        Args:
            session_id: Unique session identifier
            user_id: Optional user identifier
            
        Returns:
            ConversationSession instance
        """
        # Check cache first
        if session_id in self._sessions:
            return self._sessions[session_id]
        
        # Try to load from store
        data = await self._store.load(session_id)
        if data:
            session = ConversationSession(**data)
            self._sessions[session_id] = session
            return session
        
        # Create new session
        now = datetime.utcnow().isoformat()
        session = ConversationSession(
            session_id=session_id,
            user_id=user_id,
            turns=[],
            created_at=now,
            updated_at=now,
        )
        self._sessions[session_id] = session
        return session
    
    async def add_turn(
        self,
        session_id: str,
        role: str,
        content: str,
        mood: Optional[str] = None,
        crisis_level: Optional[str] = None,
    ) -> None:
        """
        Add a conversation turn to the session.
        
        Args:
            session_id: Session to add turn to
            role: "user" or "assistant"
            content: Message content
            mood: Detected mood (optional)
            crisis_level: Detected crisis level (optional)
        """
        session = await self.get_or_create_session(session_id)
        
        turn = ConversationTurn(
            role=role,
            content=content,
            timestamp=datetime.utcnow().isoformat(),
            mood=mood,
            crisis_level=crisis_level,
        )
        
        session.turns.append(turn)
        session.updated_at = datetime.utcnow().isoformat()
        
        # Persist to store
        await self._save_session(session)
    
    async def get_messages(
        self,
        session_id: str,
        max_turns: Optional[int] = None,
    ) -> List[BaseMessage]:
        """
        Get conversation history as LangChain messages.
        
        Args:
            session_id: Session to retrieve
            max_turns: Maximum number of recent turns to return
            
        Returns:
            List of BaseMessage objects
        """
        session = await self.get_or_create_session(session_id)
        
        turns = session.turns
        if max_turns and len(turns) > max_turns:
            turns = turns[-max_turns:]
        
        messages = []
        for turn in turns:
            if turn.role == "user":
                messages.append(HumanMessage(content=turn.content))
            else:
                messages.append(AIMessage(content=turn.content))
        
        return messages
    
    async def get_context_summary(self, session_id: str) -> Optional[str]:
        """
        Get a summary of the conversation for context.
        
        Args:
            session_id: Session to summarize
            
        Returns:
            Summary string or None if no summary available
        """
        session = await self.get_or_create_session(session_id)
        return session.summary
    
    async def _save_session(self, session: ConversationSession) -> None:
        """Save session to persistent store."""
        data = {
            "session_id": session.session_id,
            "user_id": session.user_id,
            "turns": [asdict(t) for t in session.turns],
            "created_at": session.created_at,
            "updated_at": session.updated_at,
            "summary": session.summary,
            "metadata": session.metadata,
        }
        await self._store.save(session.session_id, data)
    
    async def clear_session(self, session_id: str) -> None:
        """Clear all data for a session."""
        await self._store.delete(session_id)
        self._sessions.pop(session_id, None)
    
    def get_turn_count(self, session_id: str) -> int:
        """Get the number of turns in a session."""
        if session_id in self._sessions:
            return len(self._sessions[session_id].turns)
        return 0
