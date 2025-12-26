"""
RAG Configuration for Cycology Agent.

Configures Pinecone vector database connection and index settings.
"""

import os
from typing import Optional
from functools import lru_cache

from pydantic_settings import BaseSettings


class RAGSettings(BaseSettings):
    """RAG configuration settings."""
    
    # Pinecone
    pinecone_api_key: Optional[str] = None
    pinecone_index_name: str = "cycology-mental-health"
    pinecone_cloud: str = "aws"
    pinecone_region: str = "us-east-1"
    
    # Embeddings
    embedding_model: str = "all-MiniLM-L6-v2"  # Sentence-transformers model
    embedding_dimension: int = 384  # Dimension for all-MiniLM-L6-v2
    
    # Retrieval
    default_top_k: int = 5
    similarity_threshold: float = 0.7
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


@lru_cache()
def get_rag_settings() -> RAGSettings:
    """Get cached RAG settings."""
    return RAGSettings()


rag_settings = get_rag_settings()


def get_pinecone_client():
    """
    Get Pinecone client instance.
    
    Returns:
        Pinecone client or None if not configured
    """
    if not rag_settings.pinecone_api_key:
        print("⚠ Pinecone API key not configured. Set PINECONE_API_KEY in .env")
        return None
    
    try:
        from pinecone import Pinecone
        
        pc = Pinecone(api_key=rag_settings.pinecone_api_key)
        return pc
    except ImportError:
        print("⚠ pinecone-client not installed. Run: pip install pinecone-client")
        return None
    except Exception as e:
        print(f"⚠ Error connecting to Pinecone: {e}")
        return None


def get_or_create_index():
    """
    Get or create the Pinecone index for mental health data.
    
    Returns:
        Pinecone index or None if not available
    """
    pc = get_pinecone_client()
    if not pc:
        return None
    
    try:
        # Check if index exists
        existing_indexes = pc.list_indexes()
        index_names = [idx.name for idx in existing_indexes]
        
        if rag_settings.pinecone_index_name not in index_names:
            # Create new index
            print(f"Creating Pinecone index: {rag_settings.pinecone_index_name}")
            
            from pinecone import ServerlessSpec
            
            pc.create_index(
                name=rag_settings.pinecone_index_name,
                dimension=rag_settings.embedding_dimension,
                metric="cosine",
                spec=ServerlessSpec(
                    cloud=rag_settings.pinecone_cloud,
                    region=rag_settings.pinecone_region
                )
            )
            print(f"✓ Created index: {rag_settings.pinecone_index_name}")
        
        # Get index
        index = pc.Index(rag_settings.pinecone_index_name)
        return index
        
    except Exception as e:
        print(f"⚠ Error with Pinecone index: {e}")
        return None


def check_pinecone_status() -> dict:
    """
    Check Pinecone connection and index status.
    
    Returns:
        Status dictionary
    """
    status = {
        "configured": bool(rag_settings.pinecone_api_key),
        "connected": False,
        "index_exists": False,
        "vector_count": 0,
    }
    
    if not status["configured"]:
        return status
    
    try:
        pc = get_pinecone_client()
        if pc:
            status["connected"] = True
            
            # Check index
            existing_indexes = pc.list_indexes()
            index_names = [idx.name for idx in existing_indexes]
            
            if rag_settings.pinecone_index_name in index_names:
                status["index_exists"] = True
                index = pc.Index(rag_settings.pinecone_index_name)
                stats = index.describe_index_stats()
                status["vector_count"] = stats.total_vector_count
    except Exception as e:
        status["error"] = str(e)
    
    return status
