# 🧠 Psychology Agent

> **An AI-powered mental health support companion** - A free, anonymous platform helping those who feel alone, depressed, or need someone to talk to.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Made with Love](https://img.shields.io/badge/Made%20with-❤️-red.svg)]()
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)]()

---

## 🌟 Vision

**Psychology Agent** is an NGO initiative providing free mental health support to anyone who needs it. We believe everyone deserves someone to listen, understand, and stand by them during difficult times.

### Who is this for?
- 💙 People feeling lonely or isolated
- 💚 Those going through mental health challenges
- 💛 Anyone needing a non-judgmental space to talk
- 💜 People who want support before seeing a professional

---

## ✨ Features

### Phase 1: AI Companion (MVP)
- 🤖 **Empathetic AI Chatbot** - Trained on psychology principles, always available
- 🔒 **Anonymous & Private** - No real names required, your data is safe
- 🚨 **Crisis Detection** - AI identifies when you need immediate help
- 👨‍⚕️ **Professional Escalation** - Seamlessly connect to real psychologists

### Phase 2: Enhanced Communication
- 🎤 Voice Chat - Talk instead of type
- 📹 Video Sessions - Face-to-face with professionals
- 📅 Appointment Booking - Schedule at your convenience

### Phase 3: Wellness Tools
- 📊 Mood Tracking & Journaling
- 🧘 Breathing exercises & Meditation
- 📚 Self-help Resource Library
- 👥 Anonymous Peer Support Groups

---

## 🛠️ Tech Stack (100% FREE)

| Component | Technology |
|-----------|------------|
| **Frontend** | Next.js + TypeScript + Tailwind CSS |
| **Backend** | FastAPI (Python) |
| **AI Agent** | LangGraph + LangChain |
| **LLM** | Ollama (dev) / Groq + Gemini Free (prod) |
| **Database** | MongoDB (via Docker) |
| **Containerization** | Docker + Docker Compose |
| **Hosting** | Vercel + Render (Free tier) |

---

## 🐳 Why Docker?

Our team uses different operating systems (Linux & Windows). Docker ensures:
- ✅ **Same environment everywhere** - No "works on my machine" issues
- ✅ **One-command setup** - Just `docker-compose up`
- ✅ **No dependency hell** - Python/Node versions don't clash
- ✅ **Includes database** - MongoDB runs automatically

> 📖 **New to the project?** Read the [Complete Project Documentation](docs/PROJECT_DOCS.md) for detailed explanations of everything!

---

## 👥 Team

| Member | Role | Focus Area |
|--------|------|------------|
| **Myth** | Project Lead / AI Engineer | AI Agent, Core Architecture |
| **Thushara** | Frontend Developer | UI/UX, React Components |
| **Vignesh** | Backend Developer | API, Database, Auth |

---

## 📁 Project Structure

```
psychology-agent/
├── frontend/          # 🔵 Next.js app (Thushara)
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── styles/
│   └── package.json
│
├── backend/           # 🟢 FastAPI server (Vignesh)
│   ├── app/
│   │   ├── api/
│   │   ├── models/
│   │   └── services/
│   └── requirements.txt
│
├── agent/             # 🔴 AI Agent (Myth)
│   ├── core/
│   ├── prompts/
│   └── tools/
│
├── shared/            # 🟡 Shared types
└── docs/              # 📚 Documentation
```

---

## 🚀 Complete Setup Guide (Docker)

> **Why Docker?** Works the same on Linux, Windows, and Mac. No "it works on my machine" issues!

### 📋 Prerequisites

Before you begin, ensure you have the following installed:

| Requirement | Windows/Mac | Linux | Check Command |
|-------------|-------------|-------|---------------|
| **Docker** | [Docker Desktop](https://www.docker.com/products/docker-desktop/) | `sudo apt install docker.io` | `docker --version` |
| **Docker Compose** | Included with Docker Desktop | `sudo apt install docker-compose-plugin` or download from [GitHub](https://github.com/docker/compose/releases) | `docker-compose --version` |
| **Git** | [Git for Windows](https://git-scm.com/) | `sudo apt install git` | `git --version` |

**Optional:**
- [Ollama](https://ollama.ai/) - For running LLMs locally (free, no API key needed)
- Groq API Key - Get free at [console.groq.com](https://console.groq.com)
- Google Gemini API Key - Get free at [ai.google.dev](https://ai.google.dev)

---

### 🔧 Step-by-Step Installation

#### Step 1: Clone the Repository
```bash
git clone https://github.com/Mithun095/Psychology-Agent.git
cd Psychology-Agent
```

#### Step 2: Configure Environment Variables
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your API keys (optional but recommended)
nano .env   # or use any text editor
```

**Inside `.env`, configure:**
```env
# At least ONE of these is required for AI responses:
GROQ_API_KEY=your-groq-api-key-here      # Free: https://console.groq.com
GOOGLE_API_KEY=your-gemini-api-key-here  # Free: https://ai.google.dev

# These are auto-configured (no changes needed)
DATABASE_URL=mongodb://mongo:27017/psychology
REDIS_URL=redis://redis:6379
```

#### Step 3: Start All Services
```bash
# Build and start all containers (first time takes ~5-10 minutes)
docker-compose up --build

# Or run in background (detached mode)
docker-compose up -d --build
```

#### Step 4: Verify Everything is Running
```bash
# Check all containers are up
docker ps

# Expected output: 5 containers running
# - psychology-frontend
# - psychology-backend
# - psychology-agent
# - psychology-mongo
# - psychology-redis
```

---

### 🌐 Access the Application

Once all containers are running, access these URLs in your browser:

| Service | URL | Description |
|---------|-----|-------------|
| 🖥️ **Frontend** | http://localhost:3000 | User interface |
| 🔌 **Backend API** | http://localhost:8000 | REST API endpoints |
| 📚 **API Docs** | http://localhost:8000/docs | Swagger/OpenAPI documentation |
| 🤖 **AI Agent** | http://localhost:8001 | AI agent service |
| 💾 **MongoDB** | localhost:27017 | Database (internal) |
| ⚡ **Redis** | localhost:6379 | Cache (internal) |

---

### 🧪 Test the AI Agent

You can test the AI agent directly using curl:

```bash
# Health check
curl http://localhost:8001/health

# Send a test message
curl -X POST http://localhost:8001/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, I am feeling stressed today"}'
```

**Expected response:**
```json
{
  "response": "I'm here to listen. Can you tell me more about what's causing you stress?",
  "mood": "anxious",
  "crisis_level": "none",
  "should_escalate": false
}
```

---

### 🛠️ Docker Commands Reference

```bash
# ===== STARTING =====
docker-compose up              # Start all services (foreground)
docker-compose up -d           # Start in background (detached)
docker-compose up --build      # Rebuild images and start

# ===== MONITORING =====
docker ps                      # List running containers
docker-compose logs -f         # View all logs (follow mode)
docker-compose logs backend    # View specific service logs
docker-compose logs agent      # View AI agent logs

# ===== STOPPING =====
docker-compose stop            # Stop containers (keep data)
docker-compose down            # Stop and remove containers
docker-compose down -v         # Stop and remove everything (including data!)

# ===== MAINTENANCE =====
docker-compose restart         # Restart all services
docker-compose build --no-cache # Rebuild without cache
docker system prune -a         # Clean up unused Docker resources
```

---

### ❗ Troubleshooting

#### Port Already in Use
```bash
# If you see "port already in use" error:
# Check what's using the port (e.g., 27017 for MongoDB)
sudo lsof -i :27017

# Stop the conflicting service
sudo systemctl stop mongod  # For system MongoDB
```

#### Container Won't Start
```bash
# Check container logs for errors
docker-compose logs <service-name>

# Rebuild from scratch
docker-compose down -v
docker-compose up --build
```

#### API Keys Not Working
- Ensure `.env` file exists in the root directory
- Check that API keys don't have extra spaces or quotes
- Restart containers after changing `.env`: `docker-compose restart`

---

### 💻 Development Workflow

For active development, the containers mount your local code as volumes, so changes reflect immediately:

```bash
# Start services
docker-compose up -d

# Make code changes locally
# Changes in frontend/ backend/ agent/ auto-reload

# If you add new dependencies:
docker-compose up --build

# View logs while developing
docker-compose logs -f agent    # Watch AI agent logs
docker-compose logs -f backend  # Watch backend logs
```

---

## 🤝 Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for our git workflow and contribution guidelines.

### For Team Members
Check your assigned workflow file in `.agent/workflows/`:
- **Thushara**: `.agent/workflows/thushara-frontend.md`
- **Vignesh**: `.agent/workflows/vignesh-backend.md`
- **Myth**: `.agent/workflows/myth-agent.md`

---

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

---

## 💚 Support This Initiative

If you believe in our mission to make mental health support accessible to everyone, consider:
- ⭐ Starring this repo
- 🤝 Contributing code or ideas
- 📢 Spreading the word

---

<p align="center">
  <b>Remember: You are not alone. We're here to help. 💚</b>
</p>
