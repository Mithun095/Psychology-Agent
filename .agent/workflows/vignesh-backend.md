---
description: Backend development workflow for Vignesh
---

# 🟢 Vignesh's Backend Development Workflow

Welcome to the Cycology Agent project! This is your workflow guide for backend development.

## Your Role
You are the **Backend Developer** responsible for building the API, database, and real-time features of the Cycology Agent platform.

## Your Directory
You can **ONLY** work in: `backend/`

---

## 🚀 Getting Started

### Step 1: Clone and Setup Branch
```bash
git clone https://github.com/your-org/cycology-agent.git
cd cycology-agent
git checkout -b feature/backend
git push -u origin feature/backend
```

### Step 2: Start with Docker (Recommended)
```bash
# From project root
cp .env.example .env
docker-compose up --build

# Backend API at http://localhost:8000
# API Docs at http://localhost:8000/docs
# MongoDB available at localhost:27017
# Changes in backend/ auto-reload!
```

### Alternative: Run Backend Only
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

---

## 📋 Your Tasks

### Phase 1: Setup & Core API
- [ ] Initialize FastAPI project structure
- [ ] Setup SQLAlchemy/MongoDB connection
- [ ] Create base models (User, Message, Session)
- [ ] Setup CORS and security middleware

### Phase 2: Authentication
- [ ] Implement anonymous user creation
- [ ] Add JWT token generation
- [ ] Create optional social auth (Google)
- [ ] Build user session management

### Phase 3: Chat API
- [ ] Create WebSocket endpoint for real-time chat
- [ ] Build message storage and retrieval API
- [ ] Implement chat session management
- [ ] Add message history pagination

### Phase 4: Professional Features
- [ ] Create psychologist registration API
- [ ] Build appointment booking system
- [ ] Implement availability calendar API
- [ ] Add video call session management

---

## 🏗️ Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI entry point
│   ├── config.py            # Environment config
│   ├── api/
│   │   ├── v1/
│   │   │   ├── auth.py      # Authentication routes
│   │   │   ├── chat.py      # Chat routes
│   │   │   ├── users.py     # User routes
│   │   │   └── appointments.py
│   │   └── deps.py          # Dependencies
│   ├── models/
│   │   ├── user.py
│   │   ├── message.py
│   │   └── session.py
│   ├── schemas/
│   │   ├── user.py
│   │   └── message.py
│   ├── services/
│   │   ├── auth.py
│   │   ├── chat.py
│   │   └── ai_bridge.py     # Bridge to AI agent
│   └── utils/
│       ├── security.py
│       └── websocket.py
├── requirements.txt
├── .env.example
└── Dockerfile
```

---

## 📡 API Endpoints to Implement

### Authentication
```
POST /api/v1/auth/anonymous     # Create anonymous user
POST /api/v1/auth/register      # Optional full registration
POST /api/v1/auth/login         # Login
POST /api/v1/auth/refresh       # Refresh token
```

### Chat
```
WS   /api/v1/chat/ws/{user_id}  # WebSocket connection
GET  /api/v1/chat/history       # Get chat history
POST /api/v1/chat/session       # Create new session
```

### Users
```
GET  /api/v1/users/me           # Get current user
PATCH /api/v1/users/me          # Update profile
```

### Appointments
```
GET  /api/v1/appointments       # List appointments
POST /api/v1/appointments       # Book appointment
GET  /api/v1/doctors/available  # Get available slots
```

---

## 🤖 Antigravity Prompt

Copy and paste this prompt into Antigravity to get started:

```
I am Vignesh, the Backend Developer for the Cycology Agent project.

This is an AI-powered mental health support platform (NGO initiative) that provides:
- Empathetic AI chatbot for people feeling lonely/depressed
- Anonymous & private conversations
- Connection to real psychologists when needed
- Video/voice call capabilities

My responsibility is building the backend in the `backend/` directory using:
- FastAPI (Python)
- MongoDB with Motor (async) or Supabase
- WebSocket for real-time chat
- JWT for authentication

IMPORTANT: I can ONLY edit files in the `backend/` directory. Never touch other directories.

The AI agent (built by Myth) will expose an API that I need to integrate with. I should create a bridge service to communicate with the agent.

My current priority tasks:
1. Initialize FastAPI project with proper structure
2. Setup MongoDB/Supabase connection
3. Create authentication system (supporting anonymous users)
4. Build WebSocket endpoint for real-time chat

Please help me start by setting up the project structure and creating the core API skeleton.
```

---

## 🔄 Git Workflow

```bash
# Before starting work each day:
git checkout main
git pull origin main
git checkout feature/backend
git merge main

# After making changes:
git add .
git commit -m "feat: description"
git push origin feature/backend

# Create PR when ready for review
```

---

## 🔌 Integration Points

Your backend needs to communicate with:

1. **Frontend** (Thushara) - REST API + WebSocket
2. **AI Agent** (Myth) - Internal API call to get AI responses

Create a bridge service in `services/ai_bridge.py`:
```python
async def get_ai_response(user_id: str, message: str) -> str:
    """
    Call the AI agent to get a response.
    Myth will provide the API endpoint.
    """
    # TODO: Implement when agent API is ready
    pass
```

---

## ❓ Questions?
Contact Myth (Project Lead) for any architectural decisions or questions.
