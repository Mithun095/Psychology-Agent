# Psychology AI Agent

Empathetic mental health support chatbot powered by LangGraph with RAG (Retrieval-Augmented Generation).

## Features

- 🧠 **Psychology-focused prompts** - Warm, validating, non-judgmental responses
- 🚨 **Crisis detection** - Multi-layer keyword and pattern matching
- 💭 **Mood analysis** - Real-time sentiment tracking
- 🔄 **Multi-LLM support** - Ollama (local) → Groq → Gemini fallback
- 💾 **Conversation memory** - Redis-backed session persistence
- 📚 **RAG System** - Retrieves similar counseling examples for better responses
- 🔍 **Pinecone Vector DB** - Semantic search across thousands of therapy conversations

## Quick Start

### 1. Setup Environment

```bash
cd agent

# Copy environment template
cp .env.example .env

# Edit .env and add your API keys
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure LLM (choose one)

**Option A: Ollama (Local - Recommended for Development)**
```bash
# Install Ollama: https://ollama.ai
ollama serve
ollama pull llama3.2
```

**Option B: Groq (Free Cloud API)**
```bash
# Get free API key: https://console.groq.com
# Add to .env: GROQ_API_KEY=your-key-here
```

**Option C: Google Gemini (Free Cloud API)**
```bash
# Get free API key: https://ai.google.dev
# Add to .env: GOOGLE_API_KEY=your-key-here
```

### 4. Setup RAG (Optional but Recommended)

```bash
# Download training data
cd data/scripts
python download_data.py

# Preprocess data
python preprocess.py

# Ingest to Pinecone (requires PINECONE_API_KEY in .env)
cd ../..
python -m rag.ingestion
```

### 5. Run the Agent

```bash
python main.py
```

### 6. Test the API

```bash
# Basic chat
curl -X POST http://localhost:8001/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "I have been feeling really stressed lately"}'

# Check RAG status
curl http://localhost:8001/rag/status
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/chat` | POST | Send message, get empathetic response |
| `/health` | GET | Service health and available LLMs |
| `/rag/status` | GET | RAG/Pinecone connection status |
| `/session/{id}` | GET | Get session info |
| `/session/{id}` | DELETE | End/clear session |
| `/docs` | GET | Interactive API documentation |

## Architecture

```
agent/
├── core/
│   ├── agent.py      # LangGraph agent with nodes
│   ├── state.py      # Pydantic state models
│   └── config.py     # Multi-LLM configuration
├── prompts/
│   ├── system.py     # Psychology-focused prompts
│   └── templates.py  # Response templates & resources
├── tools/
│   ├── crisis.py     # Crisis detection
│   ├── mood.py       # Mood analysis
│   └── escalation.py # Professional referral logic
├── memory/
│   └── conversation.py  # Redis-backed memory
├── rag/                  # NEW: RAG System
│   ├── config.py        # Pinecone configuration
│   ├── embeddings.py    # Sentence-transformer embeddings
│   ├── ingestion.py     # Data ingestion pipeline
│   └── retriever.py     # Vector search
├── data/                 # NEW: Training Data
│   ├── raw/             # Downloaded datasets
│   ├── processed/       # Cleaned data
│   └── scripts/         # Download & preprocessing
└── main.py              # FastAPI entry point
```

## RAG System

The RAG system improves response quality by retrieving relevant counseling examples:

1. **Data Sources** (FREE, open datasets):
   - Hugging Face: `amod/mental_health_counseling_conversations`
   - Kaggle: Mental Health Counseling Conversations
   - Counsel-Chat dataset

2. **Embeddings**: Sentence-Transformers (runs locally, no API costs)
   - Model: `all-MiniLM-L6-v2`
   - Dimension: 384

3. **Vector DB**: Pinecone (free tier: 100K vectors)
   - Semantic similarity search
   - Topic filtering (depression, anxiety, etc.)

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GROQ_API_KEY` | No* | Groq API key |
| `GOOGLE_API_KEY` | No* | Google Gemini API key |
| `PINECONE_API_KEY` | No | Pinecone API key for RAG |
| `PINECONE_INDEX_NAME` | No | Pinecone index name |
| `REDIS_URL` | No | Redis connection URL |

*At least one LLM provider should be configured, or use Ollama locally.

## Docker

```bash
# From project root
docker-compose up agent

# Or build standalone
cd agent
docker build -t psychology-agent .
docker run -p 8001:8001 --env-file .env psychology-agent
```

## Crisis Detection Levels

| Level | Description | Response |
|-------|-------------|----------|
| CRITICAL | Immediate danger signals | Emergency resources + intervention |
| HIGH | Serious distress indicators | Strong push for professional help |
| MEDIUM | Significant distress | Offer resources, monitor closely |
| LOW | Mild distress | Supportive, attentive listening |
| NONE | Normal conversation | Standard empathetic dialogue |

## Development

```bash
# Install dev dependencies
pip install pytest black flake8

# Run tests
pytest

# Format code
black .
```
