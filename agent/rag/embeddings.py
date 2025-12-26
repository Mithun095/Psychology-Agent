"""
Embedding Generation for Cycology Agent.

Uses Sentence-Transformers for FREE, local embedding generation.
No API costs, runs entirely on your machine.
"""

from typing import List, Union
import numpy as np


class EmbeddingModel:
    """
    Embedding model using Sentence-Transformers.
    
    Model: all-MiniLM-L6-v2
    - Dimension: 384
    - Fast and efficient
    - Good quality for semantic search
    - Runs locally (no API costs)
    """
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the embedding model.
        
        Args:
            model_name: Sentence-transformers model name
        """
        self.model_name = model_name
        self._model = None
    
    @property
    def model(self):
        """Lazy load the model."""
        if self._model is None:
            try:
                from sentence_transformers import SentenceTransformer
                print(f"Loading embedding model: {self.model_name}")
                self._model = SentenceTransformer(self.model_name)
                print(f"✓ Model loaded (dimension: {self._model.get_sentence_embedding_dimension()})")
            except ImportError:
                raise ImportError(
                    "sentence-transformers not installed. "
                    "Run: pip install sentence-transformers"
                )
        return self._model
    
    def embed(self, texts: Union[str, List[str]]) -> np.ndarray:
        """
        Generate embeddings for text(s).
        
        Args:
            texts: Single text or list of texts
            
        Returns:
            Numpy array of embeddings
        """
        if isinstance(texts, str):
            texts = [texts]
        
        embeddings = self.model.encode(
            texts,
            show_progress_bar=len(texts) > 10,
            convert_to_numpy=True
        )
        
        return embeddings
    
    def embed_query(self, query: str) -> List[float]:
        """
        Generate embedding for a search query.
        
        Args:
            query: Search query text
            
        Returns:
            List of floats (embedding vector)
        """
        embedding = self.embed(query)
        return embedding[0].tolist()
    
    def embed_documents(self, documents: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple documents.
        
        Args:
            documents: List of document texts
            
        Returns:
            List of embedding vectors
        """
        embeddings = self.embed(documents)
        return embeddings.tolist()
    
    @property
    def dimension(self) -> int:
        """Get the embedding dimension."""
        return self.model.get_sentence_embedding_dimension()


# Singleton instance
_embedding_model = None


def get_embedding_model() -> EmbeddingModel:
    """Get or create the embedding model instance."""
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = EmbeddingModel()
    return _embedding_model


def embed_text(text: str) -> List[float]:
    """
    Convenience function to embed a single text.
    
    Args:
        text: Text to embed
        
    Returns:
        Embedding vector as list of floats
    """
    model = get_embedding_model()
    return model.embed_query(text)


def embed_texts(texts: List[str]) -> List[List[float]]:
    """
    Convenience function to embed multiple texts.
    
    Args:
        texts: List of texts to embed
        
    Returns:
        List of embedding vectors
    """
    model = get_embedding_model()
    return model.embed_documents(texts)
