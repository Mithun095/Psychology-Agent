"""
Vector Search Retriever for Psychology Agent.

Retrieves relevant counseling examples from Pinecone based on semantic similarity.
"""

from typing import List, Optional
from dataclasses import dataclass

from .config import get_or_create_index, rag_settings
from .embeddings import embed_text


@dataclass
class RetrievedExample:
    """A retrieved counseling example."""
    id: str
    question: str
    response: str
    topic: str
    source: str
    score: float  # Similarity score (0-1)
    
    def format_for_prompt(self) -> str:
        """Format as context for the LLM prompt."""
        return f"""**Similar Situation:**
User said: "{self.question}"
Counselor responded: "{self.response}"
"""


class MentalHealthRetriever:
    """
    Retrieves relevant counseling examples from the vector database.
    
    Uses semantic similarity to find past conversations that are
    relevant to the current user message.
    """
    
    def __init__(self):
        """Initialize the retriever."""
        self._index = None
    
    @property
    def index(self):
        """Lazy load the Pinecone index."""
        if self._index is None:
            self._index = get_or_create_index()
        return self._index
    
    def retrieve(
        self,
        query: str,
        top_k: int = None,
        topic_filter: Optional[str] = None,
        min_score: float = None,
    ) -> List[RetrievedExample]:
        """
        Retrieve relevant counseling examples.
        
        Args:
            query: User's message to find similar examples for
            top_k: Number of results to return (default from settings)
            topic_filter: Filter by topic (depression, anxiety, etc.)
            min_score: Minimum similarity score (default from settings)
            
        Returns:
            List of RetrievedExample objects
        """
        if self.index is None:
            return []
        
        top_k = top_k or rag_settings.default_top_k
        min_score = min_score or rag_settings.similarity_threshold
        
        # Generate query embedding
        query_embedding = embed_text(query)
        
        # Build filter if topic specified
        filter_dict = None
        if topic_filter:
            filter_dict = {"topic": {"$eq": topic_filter}}
        
        # Query Pinecone
        try:
            results = self.index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True,
                filter=filter_dict,
            )
        except Exception as e:
            print(f"⚠ Retrieval error: {e}")
            return []
        
        # Convert to RetrievedExample objects
        examples = []
        for match in results.matches:
            if match.score >= min_score:
                metadata = match.metadata or {}
                examples.append(RetrievedExample(
                    id=match.id,
                    question=metadata.get("question", ""),
                    response=metadata.get("response", ""),
                    topic=metadata.get("topic", "general"),
                    source=metadata.get("source", "unknown"),
                    score=match.score,
                ))
        
        return examples
    
    def get_context_for_prompt(
        self,
        query: str,
        max_examples: int = 3,
    ) -> str:
        """
        Get formatted context string for LLM prompt.
        
        Args:
            query: User's message
            max_examples: Maximum examples to include
            
        Returns:
            Formatted context string
        """
        examples = self.retrieve(query, top_k=max_examples)
        
        if not examples:
            return ""
        
        context_parts = [
            "\n## Relevant Counseling Examples",
            "Here are some examples of how trained counselors have responded to similar situations:",
            ""
        ]
        
        for i, example in enumerate(examples, 1):
            context_parts.append(f"### Example {i} (relevance: {example.score:.2f})")
            context_parts.append(example.format_for_prompt())
        
        context_parts.append(
            "\nUse these examples as inspiration, but craft your own unique, "
            "personalized response for this user's specific situation."
        )
        
        return "\n".join(context_parts)


# Singleton instance
_retriever = None


def get_retriever() -> MentalHealthRetriever:
    """Get or create the retriever instance."""
    global _retriever
    if _retriever is None:
        _retriever = MentalHealthRetriever()
    return _retriever


def retrieve_examples(query: str, top_k: int = 3) -> List[RetrievedExample]:
    """
    Convenience function to retrieve examples.
    
    Args:
        query: User's message
        top_k: Number of results
        
    Returns:
        List of RetrievedExample objects
    """
    retriever = get_retriever()
    return retriever.retrieve(query, top_k=top_k)


def get_rag_context(query: str) -> str:
    """
    Convenience function to get RAG context for prompts.
    
    Args:
        query: User's message
        
    Returns:
        Formatted context string
    """
    retriever = get_retriever()
    return retriever.get_context_for_prompt(query)
