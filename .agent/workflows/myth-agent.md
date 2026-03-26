---
description: AI Agent development workflow for Myth (Project Lead)
---

# 🔴 Myth's AI Agent Development Workflow

You are the **Project Lead & AI Engineer** for the Cycology Agent project.

## Your Directories
- `agent/` - AI Agent code
- `shared/` - Shared types and constants
- Root files - README, CONTRIBUTING, configs

---

## 📋 Your Tasks

### Phase 1: Core Agent
- [ ] Setup LangGraph project structure
- [ ] Create psychology-focused system prompts
- [ ] Implement conversation memory
- [ ] Build crisis detection logic

### Phase 2: Advanced Features
- [ ] Add mood analysis from messages
- [ ] Implement escalation decision making
- [ ] Create tool for booking appointments
- [ ] Build integration bridge with backend

### Phase 3: Optimization
- [ ] Fine-tune prompts for empathy
- [ ] Add safety guardrails
- [ ] Implement fallback LLM handling
- [ ] Performance optimization

---

## 🤖 Antigravity Prompt

```
I am Myth, the Project Lead and AI Engineer for Cycology Agent.

This is an AI mental health support platform. I am responsible for:
- Building the LangGraph-based AI agent in `agent/`
- Creating psychology-focused prompts
- Implementing crisis detection
- Managing the overall project architecture

I am using FREE LLM options:
- Development: Ollama with Llama 3.2 or Mistral
- Production: Groq free tier + Google Gemini as fallback

Please help me build the core AI agent with empathetic responses and crisis detection.
```

---

## 🎯 Architecture

```
agent/
├── core/
│   ├── agent.py          # Main LangGraph agent
│   ├── state.py          # Agent state management
│   └── config.py         # LLM configuration
├── prompts/
│   ├── system.py         # System prompts
│   └── templates.py      # Response templates
├── tools/
│   ├── crisis.py         # Crisis detection
│   ├── mood.py           # Mood analysis
│   └── escalation.py     # Professional escalation
├── memory/
│   └── conversation.py   # Chat memory
└── main.py               # Entry point
```
