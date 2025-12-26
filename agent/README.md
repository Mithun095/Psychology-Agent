# Cycology AI Agent

Empathetic mental health support chatbot powered by LangGraph.

## Features

- 🧠 **Psychology-focused prompts** - Warm, validating, non-judgmental responses
- 🚨 **Crisis detection** - Multi-layer keyword and pattern matching
- 💭 **Mood analysis** - Real-time sentiment tracking
- 🔄 **Multi-LLM support** - Ollama (local) → Groq → Gemini fallback
- 💾 **Conversation memory** - Redis-backed session persistence

## Quick Start

### 1. Install Dependencies

```bash
cd agent
pip install -r requirements.txt
```

### 2. Configure LLM (choose one)

**Option A: Ollama (Local - Recommended for Development)**
```bash
# Install Ollama: https://ollama.ai
ollama serve
ollama pull llama3.2
```

**Option B: Groq (Free Cloud API)**
```bash
# Get free API key: https://console.groq.com
export GROQ_API_KEY=your-key-here
```

**Option C: Google Gemini (Free Cloud API)**
```bash
# Get free API key: https://ai.google.dev
export GOOGLE_API_KEY=your-key-here
```

### 3. Run the Agent

```bash
python main.py
# Or with uvicorn:
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

### 4. Test the API

```bash
curl -X POST http://localhost:8001/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "I have been feeling really stressed lately"}'
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/chat` | POST | Send message, get empathetic response |
| `/health` | GET | Service health and available LLMs |
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
└── main.py           # FastAPI entry point
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

The agent uses LangGraph for orchestrating the conversation flow:

1. **Mood Analysis** - Detect emotional state from message
2. **Crisis Detection** - Check for concerning keywords/patterns
3. **Escalation Check** - Determine if professional help needed
4. **Response Generation** - Create empathetic LLM response
