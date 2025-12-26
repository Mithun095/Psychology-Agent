# Cycology Agent - Complete Project Documentation

> A comprehensive guide to understanding, setting up, and contributing to the Cycology Agent project.

---

## Table of Contents

1. [About the Project](#about-the-project)
2. [Why Docker?](#why-docker)
3. [Project Architecture](#project-architecture)
4. [Folder Structure Explained](#folder-structure-explained)
5. [Technology Stack](#technology-stack)
6. [Getting Started](#getting-started)
7. [Running the Project](#running-the-project)
8. [Team Structure](#team-structure)
9. [Development Workflow](#development-workflow)

---

## About the Project

### What is Cycology Agent?

**Cycology Agent** is an AI-powered mental health support platform designed as an NGO initiative. It provides a safe, anonymous space for people struggling with mental health challenges to receive support.

### The Problem We're Solving

- **Loneliness Epidemic**: Many people feel isolated and have no one to talk to
- **Mental Health Stigma**: People hesitate to seek professional help due to stigma
- **Accessibility**: Professional therapy is expensive and often inaccessible
- **24/7 Availability**: Mental health crises don't follow business hours

### Our Solution

An AI companion that:
- 🤖 **Listens without judgment** - Available 24/7
- 🔒 **Maintains privacy** - Anonymous conversations
- 💚 **Provides support** - Trained on psychology principles
- 🚨 **Detects crises** - Identifies when professional help is needed
- 👨‍⚕️ **Connects to professionals** - Seamless escalation to real psychologists

### Target Users

| User Type | Description |
|-----------|-------------|
| **Primary** | People feeling lonely, depressed, or anxious |
| **Secondary** | Anyone needing someone to talk to anonymously |
| **Professional** | Psychologists offering their services |

---

## Why Docker?

### The Problem Docker Solves

Our team works on different operating systems:
- **Myth (Lead)**: Linux
- **Thushara**: Windows  
- **Vignesh**: Windows

Without Docker, we'd face:
- ❌ "It works on my machine" problems
- ❌ Different Python/Node versions causing bugs
- ❌ Complex setup instructions for each OS
- ❌ Database installation hassles

### What Docker Does

Docker creates **containers** - lightweight virtual environments that work identically on every computer.

```
┌─────────────────────────────────────────────────┐
│                  Your Computer                   │
│  ┌───────────┐ ┌───────────┐ ┌───────────────┐  │
│  │ Frontend  │ │  Backend  │ │   AI Agent    │  │
│  │ Container │ │ Container │ │   Container   │  │
│  │ (Node.js) │ │ (Python)  │ │   (Python)    │  │
│  └───────────┘ └───────────┘ └───────────────┘  │
│  ┌───────────┐ ┌───────────┐                    │
│  │  MongoDB  │ │   Redis   │                    │
│  │ Container │ │ Container │                    │
│  └───────────┘ └───────────┘                    │
└─────────────────────────────────────────────────┘
```

### Benefits

| Benefit | Description |
|---------|-------------|
| **Consistency** | Same environment on Linux, Windows, Mac |
| **One Command** | `docker-compose up` starts everything |
| **Isolation** | Each service runs independently |
| **No Conflicts** | Different Python/Node versions don't clash |
| **Easy Setup** | New developers can start in minutes |

---

## Project Architecture

### High-Level Overview

```
┌─────────────────────────────────────────────────────────────┐
│                         USER                                 │
│                          │                                   │
│                          ▼                                   │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                    FRONTEND                            │  │
│  │              (Next.js + React)                         │  │
│  │         http://localhost:3000                          │  │
│  └───────────────────────────────────────────────────────┘  │
│                          │                                   │
│              REST API + WebSocket                            │
│                          │                                   │
│                          ▼                                   │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                    BACKEND                             │  │
│  │              (FastAPI + Python)                        │  │
│  │         http://localhost:8000                          │  │
│  └───────────────────────────────────────────────────────┘  │
│         │                                      │             │
│         │                                      │             │
│         ▼                                      ▼             │
│  ┌─────────────┐                    ┌───────────────────┐   │
│  │   MongoDB   │                    │     AI AGENT      │   │
│  │  (Database) │                    │    (LangGraph)    │   │
│  │ :27017      │                    │    :8001          │   │
│  └─────────────┘                    └───────────────────┘   │
│                                              │               │
│                                              ▼               │
│                                     ┌───────────────────┐   │
│                                     │   LLM Provider    │   │
│                                     │ (Ollama/Groq/     │   │
│                                     │  Gemini)          │   │
│                                     └───────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **User sends message** → Frontend
2. **Frontend** → WebSocket → Backend
3. **Backend** → Stores message in MongoDB
4. **Backend** → Calls AI Agent API
5. **AI Agent** → Calls LLM (Ollama/Groq/Gemini)
6. **AI Response** → Backend → Frontend → User

---

## Folder Structure Explained

```
cycology-agent/
│
├── 📁 frontend/                 # THUSHARA'S DOMAIN
│   ├── 📁 src/
│   │   ├── 📁 components/       # Reusable UI components
│   │   │   ├── ChatBubble.tsx   # Individual message bubble
│   │   │   ├── ChatInput.tsx    # Text input for messages
│   │   │   ├── Navbar.tsx       # Top navigation bar
│   │   │   └── ...
│   │   ├── 📁 pages/            # Next.js pages (routes)
│   │   │   ├── index.tsx        # Home/Landing page
│   │   │   ├── chat.tsx         # Main chat interface
│   │   │   ├── login.tsx        # Anonymous login
│   │   │   └── ...
│   │   ├── 📁 styles/           # CSS files
│   │   │   └── globals.css      # Global styles
│   │   └── 📁 hooks/            # Custom React hooks
│   │       └── useSocket.ts     # WebSocket connection hook
│   ├── 📁 public/               # Static assets (images, icons)
│   ├── Dockerfile               # Docker build instructions
│   ├── package.json             # Node.js dependencies
│   └── README.md                # Frontend-specific docs
│
├── 📁 backend/                  # VIGNESH'S DOMAIN
│   ├── 📁 app/
│   │   ├── main.py              # FastAPI entry point
│   │   ├── config.py            # Environment configuration
│   │   ├── 📁 api/
│   │   │   ├── 📁 v1/           # API version 1 routes
│   │   │   │   ├── auth.py      # Authentication endpoints
│   │   │   │   ├── chat.py      # Chat endpoints + WebSocket
│   │   │   │   ├── users.py     # User management
│   │   │   │   └── appointments.py  # Booking system
│   │   │   └── deps.py          # Dependency injection
│   │   ├── 📁 models/           # Database models
│   │   │   ├── user.py          # User model
│   │   │   ├── message.py       # Chat message model
│   │   │   └── session.py       # Chat session model
│   │   ├── 📁 schemas/          # Pydantic validation schemas
│   │   │   ├── user.py          # User request/response schemas
│   │   │   └── message.py       # Message schemas
│   │   ├── 📁 services/         # Business logic
│   │   │   ├── auth.py          # Authentication logic
│   │   │   ├── chat.py          # Chat processing logic
│   │   │   └── ai_bridge.py     # Bridge to AI Agent
│   │   └── 📁 utils/            # Helper functions
│   │       ├── security.py      # JWT, password hashing
│   │       └── websocket.py     # WebSocket manager
│   ├── Dockerfile               # Docker build instructions
│   ├── requirements.txt         # Python dependencies
│   └── README.md                # Backend-specific docs
│
├── 📁 agent/                    # MYTH'S DOMAIN
│   ├── 📁 core/
│   │   ├── agent.py             # Main LangGraph agent
│   │   ├── state.py             # Agent state management
│   │   └── config.py            # LLM configuration
│   ├── 📁 prompts/
│   │   ├── system.py            # System prompts for psychology
│   │   └── templates.py         # Response templates
│   ├── 📁 tools/
│   │   ├── crisis.py            # Crisis detection tool
│   │   ├── mood.py              # Mood analysis tool
│   │   └── escalation.py        # Professional escalation
│   ├── 📁 memory/
│   │   └── conversation.py      # Chat history management
│   ├── main.py                  # FastAPI entry for agent
│   ├── Dockerfile               # Docker build instructions
│   ├── requirements.txt         # Python dependencies
│   └── README.md                # Agent-specific docs
│
├── 📁 shared/                   # SHARED CODE (Myth manages)
│   ├── 📁 types/                # Shared TypeScript/Python types
│   └── README.md
│
├── 📁 docs/                     # DOCUMENTATION
│   └── PROJECT_DOCS.md          # This file!
│
├── 📁 .agent/                   # ANTIGRAVITY WORKFLOWS
│   └── 📁 workflows/
│       ├── thushara-frontend.md # Thushara's workflow + prompt
│       ├── vignesh-backend.md   # Vignesh's workflow + prompt
│       └── myth-agent.md        # Myth's workflow
│
├── docker-compose.yml           # Docker orchestration
├── .env.example                 # Environment template
├── README.md                    # Main project README
├── CONTRIBUTING.md              # Git workflow guide
└── .gitignore                   # Git ignore patterns
```

---

## Technology Stack

### Why These Technologies?

| Technology | Why We Chose It | Cost |
|------------|-----------------|------|
| **Next.js** | Best React framework, SSR, great DX | FREE |
| **FastAPI** | Python, async, auto-docs, AI-friendly | FREE |
| **LangGraph** | Agentic AI workflows, state management | FREE |
| **MongoDB** | Flexible schema for chat data | FREE tier |
| **Redis** | Fast caching, session storage | FREE |
| **Docker** | Cross-platform consistency | FREE |

### LLM Options (All FREE)

| Provider | Speed | Limits | Best For |
|----------|-------|--------|----------|
| **Ollama** | Medium | Unlimited | Development (local) |
| **Groq** | Very Fast | 30 req/min | Production demo |
| **Gemini** | Fast | 60 req/min | Production |

---

## Getting Started

### Prerequisites

1. **Install Docker Desktop**
   - Windows/Mac: Download from [docker.com](https://www.docker.com/products/docker-desktop/)
   - Linux: `sudo apt install docker.io docker-compose`

2. **Install Git**
   - Download from [git-scm.com](https://git-scm.com/)

3. **(Optional) Install Ollama** for local LLM
   - Download from [ollama.ai](https://ollama.ai/)
   - Run: `ollama pull llama3.2`

### Clone the Project

```bash
# Clone the repository
git clone https://github.com/your-org/cycology-agent.git

# Navigate to project
cd cycology-agent

# Copy environment file
cp .env.example .env
```

### Configure Environment

Edit `.env` file:

```env
# For Groq (get free key at console.groq.com)
GROQ_API_KEY=your-key-here

# For Gemini (get free key at ai.google.dev)
GOOGLE_API_KEY=your-key-here

# Leave empty to use Ollama (local)
```

---

## Running the Project

### Start All Services

```bash
# Build and start everything
docker-compose up --build

# Or run in background
docker-compose up -d --build
```

### Access Points

| Service | URL | Description |
|---------|-----|-------------|
| Frontend | http://localhost:3000 | Main web application |
| Backend API | http://localhost:8000 | REST API |
| API Docs | http://localhost:8000/docs | Interactive API docs |
| AI Agent | http://localhost:8001 | Agent API |
| MongoDB | localhost:27017 | Database |

### Useful Commands

```bash
# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f frontend
docker-compose logs -f backend

# Stop all services
docker-compose down

# Rebuild a specific service
docker-compose up --build frontend

# Remove everything including data
docker-compose down -v
```

### Hot Reload

All services have **hot reload** enabled:
- Edit frontend code → Browser auto-refreshes
- Edit backend code → Server auto-restarts
- Edit agent code → Agent auto-restarts

---

## Team Structure

| Member | Role | Owns | Branch |
|--------|------|------|--------|
| **Myth** | Lead + AI | `agent/`, `shared/`, root files | `main` |
| **Thushara** | Frontend | `frontend/` only | `feature/frontend` |
| **Vignesh** | Backend | `backend/` only | `feature/backend` |

### Golden Rule

> **Each person ONLY edits files in their assigned directory!**

This prevents merge conflicts entirely.

---

## Development Workflow

### For New Team Members

1. **Clone the repo**
   ```bash
   git clone https://github.com/your-org/cycology-agent.git
   cd cycology-agent
   ```

2. **Create your branch**
   ```bash
   # For Thushara:
   git checkout -b feature/frontend
   
   # For Vignesh:
   git checkout -b feature/backend
   ```

3. **Start Docker**
   ```bash
   cp .env.example .env
   docker-compose up --build
   ```

4. **Open your workflow file** in `.agent/workflows/`

5. **Copy the Antigravity prompt** and paste into Claude to start coding!

### Daily Workflow

```bash
# Start of day - sync with main
git checkout main
git pull origin main
git checkout your-branch
git merge main

# Code in your directory only!

# End of day - commit and push
git add .
git commit -m "feat: description of changes"
git push origin your-branch
```

### Creating a Pull Request

1. Push your branch
2. Go to GitHub → New Pull Request
3. Select your branch → main
4. Request review from Myth
5. Wait for approval before merging

---

## Need Help?

- **Technical Questions**: Ask in the team chat
- **Architecture Decisions**: Tag Myth
- **Git Issues**: Check CONTRIBUTING.md

---

**Happy Coding! 💚**
