"""
Download Mental Health Counseling Datasets.

Downloads data from:
1. Hugging Face: amod/mental_health_counseling_conversations
2. Kaggle (if credentials available)
3. Other open sources

Usage:
    python download_data.py
"""

import os
import json
from pathlib import Path
from typing import List, Dict

# Paths
SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent
RAW_DIR = DATA_DIR / "raw"
HF_DIR = RAW_DIR / "huggingface"
KAGGLE_DIR = RAW_DIR / "kaggle"


def download_huggingface_data():
    """Download from Hugging Face datasets."""
    print("📥 Downloading from Hugging Face...")
    
    try:
        from datasets import load_dataset
        
        # Primary dataset: amod/mental_health_counseling_conversations
        print("  Loading amod/mental_health_counseling_conversations...")
        dataset = load_dataset("Amod/mental_health_counseling_conversations")
        
        # Save to disk
        HF_DIR.mkdir(parents=True, exist_ok=True)
        output_file = HF_DIR / "mental_health_counseling.jsonl"
        
        count = 0
        with open(output_file, "w", encoding="utf-8") as f:
            for split in dataset:
                for item in dataset[split]:
                    record = {
                        "id": f"hf_{count}",
                        "question": item.get("Context", ""),
                        "response": item.get("Response", ""),
                        "source": "huggingface_amod"
                    }
                    f.write(json.dumps(record, ensure_ascii=False) + "\n")
                    count += 1
        
        print(f"  ✓ Saved {count} records to {output_file}")
        return count
        
    except ImportError:
        print("  ⚠ 'datasets' package not installed. Run: pip install datasets")
        return 0
    except Exception as e:
        print(f"  ⚠ Error downloading: {e}")
        return 0


def download_kaggle_data():
    """Download from Kaggle (requires credentials)."""
    print("📥 Downloading from Kaggle...")
    
    try:
        import kaggle
        
        KAGGLE_DIR.mkdir(parents=True, exist_ok=True)
        
        # Download mental health counseling conversations
        kaggle.api.dataset_download_files(
            "elvis23/mental-health-counseling-conversations",
            path=str(KAGGLE_DIR),
            unzip=True
        )
        
        print(f"  ✓ Downloaded to {KAGGLE_DIR}")
        return True
        
    except ImportError:
        print("  ⚠ 'kaggle' package not installed. Run: pip install kaggle")
        print("  ⚠ Also need to setup Kaggle credentials: ~/.kaggle/kaggle.json")
        return False
    except Exception as e:
        print(f"  ⚠ Error downloading: {e}")
        print("  ⚠ Make sure you have Kaggle credentials set up")
        return False


def create_sample_data():
    """Create sample counseling data for testing."""
    print("📝 Creating sample data for testing...")
    
    sample_data = [
        {
            "id": "sample_1",
            "question": "I've been feeling really anxious lately. I can't stop worrying about everything.",
            "response": "I hear you, and it sounds like anxiety has been weighing heavily on you. Constant worry can be exhausting. Can you tell me more about what specific things have been on your mind? Sometimes naming our worries can help us feel a bit more in control.",
            "topic": "anxiety",
            "source": "sample"
        },
        {
            "id": "sample_2", 
            "question": "I feel like nobody understands me. I'm so alone.",
            "response": "Feeling misunderstood and alone is incredibly painful. I want you to know that your feelings are valid, and I'm here to listen. Loneliness can feel overwhelming, but reaching out like this takes courage. What's been making you feel most isolated?",
            "topic": "loneliness",
            "source": "sample"
        },
        {
            "id": "sample_3",
            "question": "I lost my job last month and I can't seem to get out of bed anymore.",
            "response": "Losing a job is a significant loss, and it's completely understandable that you're struggling. The loss of routine, purpose, and financial security can deeply affect our mood and motivation. Be gentle with yourself during this time. What small thing might feel manageable today?",
            "topic": "depression",
            "source": "sample"
        },
        {
            "id": "sample_4",
            "question": "My partner and I keep fighting about the same things over and over.",
            "response": "Recurring conflicts in relationships can be frustrating and draining. Often, these patterns point to deeper needs that aren't being met. When you argue, what do you think you're really hoping your partner will understand about how you feel?",
            "topic": "relationships",
            "source": "sample"
        },
        {
            "id": "sample_5",
            "question": "I feel like I'm not good enough no matter what I do.",
            "response": "That critical inner voice can be so harsh and persistent. Many people struggle with feelings of not being 'enough,' and it often has roots in earlier experiences. I'm curious - whose voice does that criticism sound like? And would you speak to a friend the way you speak to yourself?",
            "topic": "self-esteem",
            "source": "sample"
        },
        {
            "id": "sample_6",
            "question": "I can't stop thinking about my past mistakes.",
            "response": "Ruminating on past mistakes is something many people experience. While reflection can be helpful, getting stuck in a loop of self-criticism isn't. What would it mean for you to acknowledge the mistake while also recognizing that you did the best you could with what you knew then?",
            "topic": "guilt",
            "source": "sample"
        },
        {
            "id": "sample_7",
            "question": "I feel overwhelmed with work and family responsibilities.",
            "response": "Juggling multiple responsibilities can leave us feeling stretched thin and exhausted. It sounds like you're carrying a heavy load. Let's think about this together - are there any responsibilities that could be delegated, postponed, or even let go of? Sometimes we need permission to not do it all.",
            "topic": "stress",
            "source": "sample"
        },
        {
            "id": "sample_8",
            "question": "I've been having panic attacks and I'm scared something is wrong with me.",
            "response": "Panic attacks can be terrifying, but I want to reassure you that they're not dangerous, even though they feel that way. Your body is having a strong anxiety response. The good news is that panic attacks are very treatable. When you feel one coming on, try to focus on slow, deep breaths. Have you talked to a doctor about these episodes?",
            "topic": "panic",
            "source": "sample"
        },
        {
            "id": "sample_9",
            "question": "I don't feel like doing anything I used to enjoy anymore.",
            "response": "Losing interest in things that used to bring you joy is a significant change worth paying attention to. This can be a sign that you need more support right now. When did you first notice this shift? Sometimes understanding the timeline can help us identify what might have triggered these feelings.",
            "topic": "anhedonia",
            "source": "sample"
        },
        {
            "id": "sample_10",
            "question": "I'm having trouble sleeping because my mind won't stop racing.",
            "response": "Racing thoughts at night is so frustrating when you just want rest. Your mind might be trying to process things it didn't have time for during the day. Have you tried keeping a notepad by your bed to write down thoughts? Sometimes 'parking' worries on paper helps quiet the mind. What usually occupies your thoughts at night?",
            "topic": "insomnia",
            "source": "sample"
        }
    ]
    
    # Save sample data
    output_file = DATA_DIR / "processed" / "sample_conversations.jsonl"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, "w", encoding="utf-8") as f:
        for item in sample_data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
    
    print(f"  ✓ Created {len(sample_data)} sample records at {output_file}")
    return len(sample_data)


def main():
    """Main download function."""
    print("=" * 60)
    print("Mental Health Counseling Data Downloader")
    print("=" * 60)
    
    total_records = 0
    
    # Download from Hugging Face
    total_records += download_huggingface_data()
    
    # Download from Kaggle (optional)
    download_kaggle_data()
    
    # Create sample data for testing
    total_records += create_sample_data()
    
    print("=" * 60)
    print(f"✓ Total records available: {total_records}")
    print("Run 'python preprocess.py' to prepare data for embeddings")
    print("=" * 60)


if __name__ == "__main__":
    main()
