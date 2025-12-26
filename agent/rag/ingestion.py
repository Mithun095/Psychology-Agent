"""
Data Ingestion Pipeline for Psychology Agent.

Loads counseling conversations and upserts them to Pinecone.
"""

import json
from pathlib import Path
from typing import List, Dict, Generator
from dataclasses import dataclass
import hashlib

from .embeddings import get_embedding_model
from .config import get_or_create_index, rag_settings


@dataclass
class CounselingRecord:
    """A single counseling conversation record."""
    id: str
    question: str
    response: str
    topic: str = "general"
    source: str = "unknown"
    
    def to_metadata(self) -> dict:
        """Convert to Pinecone metadata format."""
        return {
            "question": self.question[:1000],  # Truncate for metadata limits
            "response": self.response[:1000],
            "topic": self.topic,
            "source": self.source,
        }
    
    def get_text_for_embedding(self) -> str:
        """Get the text to generate embeddings from."""
        # Embed the question for semantic matching
        return self.question


def generate_id(text: str) -> str:
    """Generate a unique ID from text content."""
    return hashlib.md5(text.encode()).hexdigest()[:16]


def load_jsonl(file_path: Path) -> Generator[CounselingRecord, None, None]:
    """
    Load records from a JSONL file.
    
    Args:
        file_path: Path to JSONL file
        
    Yields:
        CounselingRecord objects
    """
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                data = json.loads(line.strip())
                yield CounselingRecord(
                    id=data.get("id", generate_id(data.get("question", ""))),
                    question=data.get("question", ""),
                    response=data.get("response", ""),
                    topic=data.get("topic", "general"),
                    source=data.get("source", "unknown"),
                )
            except json.JSONDecodeError:
                continue


def load_all_data(data_dir: Path = None) -> List[CounselingRecord]:
    """
    Load all counseling data from processed directory.
    
    Args:
        data_dir: Path to data directory (defaults to agent/data/processed)
        
    Returns:
        List of CounselingRecord objects
    """
    if data_dir is None:
        data_dir = Path(__file__).parent.parent / "data" / "processed"
    
    records = []
    
    # Load all JSONL files
    for jsonl_file in data_dir.glob("*.jsonl"):
        print(f"Loading {jsonl_file.name}...")
        file_records = list(load_jsonl(jsonl_file))
        records.extend(file_records)
        print(f"  Loaded {len(file_records)} records")
    
    return records


def ingest_to_pinecone(
    records: List[CounselingRecord],
    batch_size: int = 100,
) -> int:
    """
    Ingest counseling records to Pinecone.
    
    Args:
        records: List of CounselingRecord objects
        batch_size: Number of records per batch
        
    Returns:
        Number of records ingested
    """
    index = get_or_create_index()
    if index is None:
        print("⚠ Could not connect to Pinecone. Skipping ingestion.")
        return 0
    
    embedding_model = get_embedding_model()
    total_ingested = 0
    
    # Process in batches
    for i in range(0, len(records), batch_size):
        batch = records[i:i + batch_size]
        
        # Generate embeddings
        texts = [r.get_text_for_embedding() for r in batch]
        embeddings = embedding_model.embed_documents(texts)
        
        # Prepare vectors for upsert
        vectors = []
        for record, embedding in zip(batch, embeddings):
            vectors.append({
                "id": record.id,
                "values": embedding,
                "metadata": record.to_metadata(),
            })
        
        # Upsert to Pinecone
        index.upsert(vectors=vectors)
        total_ingested += len(vectors)
        
        print(f"  Ingested {total_ingested}/{len(records)} records...")
    
    print(f"✓ Total ingested: {total_ingested} records")
    return total_ingested


def ingest_all_data():
    """
    Main ingestion function - load all data and ingest to Pinecone.
    """
    print("=" * 60)
    print("Counseling Data Ingestion Pipeline")
    print("=" * 60)
    
    # Load data
    records = load_all_data()
    
    if not records:
        print("⚠ No data found. Run download_data.py first.")
        return
    
    print(f"\nTotal records to ingest: {len(records)}")
    
    # Ingest to Pinecone
    ingested = ingest_to_pinecone(records)
    
    print("=" * 60)
    print(f"✓ Ingestion complete. {ingested} records in Pinecone.")
    print("=" * 60)


if __name__ == "__main__":
    ingest_all_data()
