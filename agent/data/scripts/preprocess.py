"""
Preprocess Downloaded Data for Embedding.

Cleans, deduplicates, and formats data from various sources
into a unified JSONL format.
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Set
import hashlib


# Paths
SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"


def clean_text(text: str) -> str:
    """Clean and normalize text."""
    if not text:
        return ""
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters but keep punctuation
    text = text.strip()
    
    return text


def deduplicate(records: List[Dict]) -> List[Dict]:
    """Remove duplicate records based on question content."""
    seen: Set[str] = set()
    unique = []
    
    for record in records:
        # Create hash of question for deduplication
        question = clean_text(record.get("question", ""))
        question_hash = hashlib.md5(question.lower().encode()).hexdigest()
        
        if question_hash not in seen and len(question) > 20:  # Skip very short questions
            seen.add(question_hash)
            unique.append(record)
    
    return unique


def process_huggingface_data() -> List[Dict]:
    """Process Hugging Face mental health counseling data."""
    records = []
    hf_file = RAW_DIR / "huggingface" / "mental_health_counseling.jsonl"
    
    if not hf_file.exists():
        print(f"  ⚠ File not found: {hf_file}")
        return records
    
    with open(hf_file, "r", encoding="utf-8") as f:
        for line in f:
            try:
                data = json.loads(line.strip())
                records.append({
                    "id": data.get("id", ""),
                    "question": clean_text(data.get("question", "")),
                    "response": clean_text(data.get("response", "")),
                    "topic": detect_topic(data.get("question", "")),
                    "source": "huggingface"
                })
            except json.JSONDecodeError:
                continue
    
    print(f"  Processed {len(records)} records from Hugging Face")
    return records


def process_kaggle_data() -> List[Dict]:
    """Process Kaggle mental health data."""
    records = []
    kaggle_dir = RAW_DIR / "kaggle"
    
    if not kaggle_dir.exists():
        return records
    
    # Look for CSV files
    for csv_file in kaggle_dir.glob("*.csv"):
        try:
            import pandas as pd
            df = pd.read_csv(csv_file)
            
            # Try common column names
            q_col = None
            r_col = None
            
            for col in df.columns:
                col_lower = col.lower()
                if 'question' in col_lower or 'context' in col_lower:
                    q_col = col
                elif 'answer' in col_lower or 'response' in col_lower:
                    r_col = col
            
            if q_col and r_col:
                for idx, row in df.iterrows():
                    records.append({
                        "id": f"kaggle_{idx}",
                        "question": clean_text(str(row[q_col])),
                        "response": clean_text(str(row[r_col])),
                        "topic": detect_topic(str(row[q_col])),
                        "source": "kaggle"
                    })
        except Exception as e:
            print(f"  ⚠ Error processing {csv_file}: {e}")
    
    print(f"  Processed {len(records)} records from Kaggle")
    return records


def detect_topic(text: str) -> str:
    """Detect the mental health topic from text."""
    text_lower = text.lower()
    
    topic_keywords = {
        "anxiety": ["anxiety", "anxious", "worried", "worry", "panic", "nervous"],
        "depression": ["depressed", "depression", "sad", "hopeless", "empty", "worthless"],
        "relationships": ["relationship", "partner", "boyfriend", "girlfriend", "marriage", "divorce"],
        "stress": ["stress", "stressed", "overwhelmed", "pressure", "burnout"],
        "grief": ["grief", "loss", "death", "died", "mourning", "passed away"],
        "trauma": ["trauma", "abuse", "ptsd", "assault", "violence"],
        "self-esteem": ["self-esteem", "confidence", "inadequate", "not good enough", "failure"],
        "anger": ["angry", "anger", "rage", "furious", "frustrated"],
        "loneliness": ["lonely", "alone", "isolated", "no friends", "abandoned"],
        "addiction": ["addiction", "addicted", "alcohol", "drugs", "gambling"],
    }
    
    for topic, keywords in topic_keywords.items():
        if any(kw in text_lower for kw in keywords):
            return topic
    
    return "general"


def process_sample_data() -> List[Dict]:
    """Process sample data if it exists."""
    records = []
    sample_file = PROCESSED_DIR / "sample_conversations.jsonl"
    
    if not sample_file.exists():
        return records
    
    with open(sample_file, "r", encoding="utf-8") as f:
        for line in f:
            try:
                records.append(json.loads(line.strip()))
            except json.JSONDecodeError:
                continue
    
    print(f"  Loaded {len(records)} sample records")
    return records


def main():
    """Main preprocessing function."""
    print("=" * 60)
    print("Data Preprocessing Pipeline")
    print("=" * 60)
    
    all_records = []
    
    # Process each data source
    print("\n📊 Processing data sources...")
    all_records.extend(process_huggingface_data())
    all_records.extend(process_kaggle_data())
    all_records.extend(process_sample_data())
    
    if not all_records:
        print("\n⚠ No data found. Run download_data.py first.")
        return
    
    # Deduplicate
    print(f"\n🔍 Deduplicating {len(all_records)} records...")
    unique_records = deduplicate(all_records)
    print(f"  Unique records: {len(unique_records)}")
    
    # Filter out low quality
    quality_records = [
        r for r in unique_records
        if len(r.get("question", "")) > 20 and len(r.get("response", "")) > 50
    ]
    print(f"  After quality filter: {len(quality_records)}")
    
    # Save processed data
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    output_file = PROCESSED_DIR / "conversations.jsonl"
    
    with open(output_file, "w", encoding="utf-8") as f:
        for record in quality_records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    
    print(f"\n✓ Saved to {output_file}")
    
    # Print topic distribution
    topic_counts = {}
    for record in quality_records:
        topic = record.get("topic", "general")
        topic_counts[topic] = topic_counts.get(topic, 0) + 1
    
    print("\n📈 Topic Distribution:")
    for topic, count in sorted(topic_counts.items(), key=lambda x: -x[1]):
        print(f"  {topic}: {count}")
    
    print("=" * 60)
    print(f"✓ Preprocessing complete. {len(quality_records)} records ready.")
    print("Run 'python -m rag.ingestion' to ingest to Pinecone.")
    print("=" * 60)


if __name__ == "__main__":
    main()
