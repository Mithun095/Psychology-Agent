"""
PDF Ingestion Pipeline for Psychology Agent.

Parses PDF files from agent/data/pdf's directory, chunks the text,
generates embeddings, and upserts to Pinecone.
"""

import os
import hashlib
from pathlib import Path
from typing import List, Generator
from dataclasses import dataclass

try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None
    print("⚠ PyMuPDF not installed. Run: pip install pymupdf")

from .embeddings import get_embedding_model
from .config import get_or_create_index, rag_settings


@dataclass
class PDFChunk:
    """A chunk of text from a PDF document."""
    id: str
    text: str
    source: str  # PDF filename
    page: int
    chunk_index: int
    
    def to_metadata(self) -> dict:
        """Convert to Pinecone metadata format."""
        return {
            "text": self.text[:1000],  # Truncate for metadata limits
            "source": self.source,
            "page": self.page,
            "chunk_index": self.chunk_index,
            "content_type": "pdf",
        }


def generate_chunk_id(source: str, page: int, chunk_index: int) -> str:
    """Generate a unique ID for a chunk."""
    content = f"{source}:{page}:{chunk_index}"
    return hashlib.md5(content.encode()).hexdigest()[:16]


def extract_text_from_pdf(pdf_path: Path) -> Generator[tuple, None, None]:
    """
    Extract text from a PDF file page by page.
    
    Args:
        pdf_path: Path to PDF file
        
    Yields:
        Tuples of (page_number, text)
    """
    if fitz is None:
        print("⚠ PyMuPDF not available. Cannot extract PDF text.")
        return
    
    try:
        doc = fitz.open(str(pdf_path))
        for page_num, page in enumerate(doc):
            text = page.get_text()
            if text.strip():
                yield (page_num + 1, text)
        doc.close()
    except Exception as e:
        print(f"⚠ Error reading {pdf_path.name}: {e}")


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """
    Split text into overlapping chunks.
    
    Args:
        text: Text to chunk
        chunk_size: Target size of each chunk (in words)
        overlap: Number of words to overlap between chunks
        
    Returns:
        List of text chunks
    """
    words = text.split()
    chunks = []
    
    if len(words) <= chunk_size:
        if words:
            chunks.append(text)
        return chunks
    
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk_words = words[start:end]
        chunk = " ".join(chunk_words)
        
        # Clean up the chunk
        chunk = " ".join(chunk.split())  # Normalize whitespace
        if len(chunk) > 100:  # Only include substantial chunks
            chunks.append(chunk)
        
        start = end - overlap
    
    return chunks


def process_pdf(pdf_path: Path) -> List[PDFChunk]:
    """
    Process a single PDF into chunks.
    
    Args:
        pdf_path: Path to PDF file
        
    Returns:
        List of PDFChunk objects
    """
    chunks = []
    source = pdf_path.name
    
    print(f"  📄 Processing: {source}")
    
    for page_num, page_text in extract_text_from_pdf(pdf_path):
        # Chunk the page text
        text_chunks = chunk_text(page_text, chunk_size=400, overlap=50)
        
        for chunk_idx, text_chunk in enumerate(text_chunks):
            chunk = PDFChunk(
                id=generate_chunk_id(source, page_num, chunk_idx),
                text=text_chunk,
                source=source,
                page=page_num,
                chunk_index=chunk_idx,
            )
            chunks.append(chunk)
    
    print(f"    ✓ Created {len(chunks)} chunks from {source}")
    return chunks


def load_all_pdfs(pdf_dir: Path = None) -> List[PDFChunk]:
    """
    Load all PDFs from the pdf's directory.
    
    Args:
        pdf_dir: Path to PDF directory (defaults to agent/data/pdf's)
        
    Returns:
        List of PDFChunk objects
    """
    if pdf_dir is None:
        pdf_dir = Path(__file__).parent.parent / "data" / "pdf's"
    
    if not pdf_dir.exists():
        print(f"⚠ PDF directory not found: {pdf_dir}")
        return []
    
    all_chunks = []
    pdf_files = list(pdf_dir.glob("*.pdf"))
    
    print(f"Found {len(pdf_files)} PDF files")
    
    for pdf_path in pdf_files:
        chunks = process_pdf(pdf_path)
        all_chunks.extend(chunks)
    
    return all_chunks


def ingest_pdfs_to_pinecone(
    chunks: List[PDFChunk],
    batch_size: int = 50,
) -> int:
    """
    Ingest PDF chunks to Pinecone.
    
    Args:
        chunks: List of PDFChunk objects
        batch_size: Number of chunks per upsert batch
        
    Returns:
        Number of chunks ingested
    """
    index = get_or_create_index()
    if index is None:
        print("⚠ Could not connect to Pinecone. Skipping PDF ingestion.")
        return 0
    
    embedding_model = get_embedding_model()
    total_ingested = 0
    
    print(f"\n🔄 Ingesting {len(chunks)} chunks to Pinecone...")
    
    # Process in batches
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        
        # Generate embeddings
        texts = [chunk.text for chunk in batch]
        try:
            embeddings = embedding_model.embed_documents(texts)
        except Exception as e:
            print(f"⚠ Embedding error: {e}")
            continue
        
        # Prepare vectors for upsert
        vectors = []
        for chunk, embedding in zip(batch, embeddings):
            vectors.append({
                "id": chunk.id,
                "values": embedding,
                "metadata": chunk.to_metadata(),
            })
        
        # Upsert to Pinecone
        try:
            index.upsert(vectors=vectors)
            total_ingested += len(vectors)
            print(f"  ✓ Ingested {total_ingested}/{len(chunks)} chunks...")
        except Exception as e:
            print(f"⚠ Upsert error: {e}")
    
    print(f"✓ Total PDF chunks ingested: {total_ingested}")
    return total_ingested


def ingest_pdfs():
    """
    Main function - load all PDFs and ingest to Pinecone.
    """
    print("=" * 60)
    print("📚 PDF Ingestion Pipeline")
    print("=" * 60)
    
    # Check if PyMuPDF is available
    if fitz is None:
        print("⚠ PyMuPDF not installed. Run: pip install pymupdf")
        return 0
    
    # Load PDFs
    chunks = load_all_pdfs()
    
    if not chunks:
        print("⚠ No PDF chunks found. Check that PDFs exist in agent/data/pdf's/")
        return 0
    
    print(f"\nTotal chunks to ingest: {len(chunks)}")
    
    # Ingest to Pinecone
    ingested = ingest_pdfs_to_pinecone(chunks)
    
    print("=" * 60)
    print(f"✓ PDF Ingestion complete. {ingested} chunks in Pinecone.")
    print("=" * 60)
    
    return ingested


if __name__ == "__main__":
    ingest_pdfs()
