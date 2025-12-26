"""
LLM Configuration for Cycology Agent.

Supports multiple FREE LLM providers with automatic fallback:
1. Ollama (local) - Development default
2. Groq (cloud, free tier) - Production primary  
3. Google Gemini (cloud, free) - Fallback
"""

import os
from enum import Enum
from typing import Optional
from functools import lru_cache

from pydantic_settings import BaseSettings
from langchain_core.language_models import BaseChatModel


class LLMProvider(str, Enum):
    """Available LLM providers."""
    OLLAMA = "ollama"
    GROQ = "groq"
    GEMINI = "gemini"


class Settings(BaseSettings):
    """Agent configuration settings."""
    
    # Environment
    environment: str = "development"
    
    # Ollama (Local Development)
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.2"  # or "mistral"
    
    # Groq (Free Tier - Production)
    groq_api_key: Optional[str] = None
    groq_model: str = "llama-3.3-70b-versatile"
    
    # Google Gemini (Free Fallback)
    google_api_key: Optional[str] = None
    gemini_model: str = "gemini-1.5-flash"
    
    # Redis for Memory
    redis_url: str = "redis://localhost:6379"
    
    # Agent Settings
    max_conversation_turns: int = 50
    temperature: float = 0.7
    max_tokens: int = 1024
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()


def _create_ollama_llm() -> Optional[BaseChatModel]:
    """Create Ollama LLM instance."""
    try:
        from langchain_community.chat_models import ChatOllama
        import httpx
        
        # Check if Ollama is running
        try:
            response = httpx.get(f"{settings.ollama_base_url}/api/tags", timeout=2.0)
            if response.status_code != 200:
                return None
        except Exception:
            return None
        
        return ChatOllama(
            base_url=settings.ollama_base_url,
            model=settings.ollama_model,
            temperature=settings.temperature,
        )
    except ImportError:
        return None


def _create_groq_llm() -> Optional[BaseChatModel]:
    """Create Groq LLM instance."""
    if not settings.groq_api_key:
        return None
    
    try:
        from langchain_groq import ChatGroq
        
        return ChatGroq(
            api_key=settings.groq_api_key,
            model=settings.groq_model,
            temperature=settings.temperature,
            max_tokens=settings.max_tokens,
        )
    except ImportError:
        return None


def _create_gemini_llm() -> Optional[BaseChatModel]:
    """Create Google Gemini LLM instance."""
    if not settings.google_api_key:
        return None
    
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        return ChatGoogleGenerativeAI(
            google_api_key=settings.google_api_key,
            model=settings.gemini_model,
            temperature=settings.temperature,
            max_output_tokens=settings.max_tokens,
        )
    except ImportError:
        return None


def get_llm(preferred_provider: Optional[LLMProvider] = None) -> BaseChatModel:
    """
    Get the best available LLM with automatic fallback.
    
    Priority (unless preferred_provider specified):
    1. Development: Ollama → Groq → Gemini
    2. Production: Groq → Gemini → Ollama
    
    Args:
        preferred_provider: Force a specific provider
        
    Returns:
        Configured LLM instance
        
    Raises:
        RuntimeError: If no LLM provider is available
    """
    providers = {
        LLMProvider.OLLAMA: _create_ollama_llm,
        LLMProvider.GROQ: _create_groq_llm,
        LLMProvider.GEMINI: _create_gemini_llm,
    }
    
    # If preferred provider specified, try it first
    if preferred_provider:
        llm = providers[preferred_provider]()
        if llm:
            return llm
    
    # Determine fallback order based on environment
    if settings.environment == "development":
        order = [LLMProvider.OLLAMA, LLMProvider.GROQ, LLMProvider.GEMINI]
    else:
        order = [LLMProvider.GROQ, LLMProvider.GEMINI, LLMProvider.OLLAMA]
    
    # Try each provider in order
    for provider in order:
        llm = providers[provider]()
        if llm:
            print(f"✓ Using LLM provider: {provider.value}")
            return llm
    
    raise RuntimeError(
        "No LLM provider available. Please either:\n"
        "1. Start Ollama locally (ollama serve)\n"
        "2. Set GROQ_API_KEY environment variable\n"
        "3. Set GOOGLE_API_KEY environment variable"
    )


def get_available_providers() -> list[LLMProvider]:
    """Check which LLM providers are currently available."""
    available = []
    
    if _create_ollama_llm():
        available.append(LLMProvider.OLLAMA)
    if _create_groq_llm():
        available.append(LLMProvider.GROQ)
    if _create_gemini_llm():
        available.append(LLMProvider.GEMINI)
    
    return available
