# Mental Health Counseling Training Data

This directory contains training data for the Cycology mental health support agent.

## Data Sources

| Source | Description | Size | License |
|--------|-------------|------|---------|
| [amod/mental_health_counseling](https://huggingface.co/datasets/amod/mental_health_counseling_conversations) | Real counselor Q&A pairs | ~3K | Open |
| [Kaggle Mental Health](https://www.kaggle.com/datasets/elvis23/mental-health-counseling-conversations) | Therapy conversations | ~3.5K | CC0 |
| Counsel-Chat | Platform conversations | ~2K | Research |

## Structure

```
data/
├── raw/                    # Original downloaded data (gitignored)
│   ├── kaggle/
│   ├── huggingface/
│   └── counselchat/
├── processed/              # Cleaned and formatted (gitignored)
│   └── conversations.jsonl
└── scripts/
    ├── download_data.py    # Download datasets
    ├── preprocess.py       # Clean and format
    └── generate_embeddings.py
```

## Usage

### 1. Download Data

```bash
cd scripts
python download_data.py
```

### 2. Preprocess

```bash
python preprocess.py
```

### 3. Generate Embeddings

```bash
python generate_embeddings.py
```

## Data Format

After preprocessing, all data is stored in JSONL format:

```json
{
  "id": "unique-id",
  "question": "User's question or message",
  "response": "Counselor's response",
  "topic": "depression|anxiety|relationships|...",
  "source": "kaggle|huggingface|counselchat"
}
```

## Privacy Note

All data is anonymized and collected from public sources or platforms where users consented to data usage for research purposes.
