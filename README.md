# 🧠 Cycology Agent

> **An AI-powered mental health support companion** - A free, anonymous platform helping those who feel alone, depressed, or need someone to talk to.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Made with Love](https://img.shields.io/badge/Made%20with-❤️-red.svg)]()
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)]()

---

## 🌟 Vision

**Cycology Agent** is an NGO initiative providing free mental health support to anyone who needs it. We believe everyone deserves someone to listen, understand, and stand by them during difficult times.

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
cycology-agent/
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

## 🚀 Quick Start (Docker)

> **Why Docker?** Works the same on Linux, Windows, and Mac. No "it works on my machine" issues!

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Windows/Mac) or Docker Engine (Linux)
- [Ollama](https://ollama.ai/) (optional, for local LLM)

### One-Command Setup

```bash
# Clone the repository
git clone https://github.com/your-org/cycology-agent.git
cd cycology-agent

# Copy environment file
cp .env.example .env

# Start everything with Docker! 🐳
docker-compose up --build
```

### Access the App
| Service | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |
| AI Agent | http://localhost:8001 |

### Useful Commands
```bash
# Start in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Rebuild after code changes
docker-compose up --build

# Remove everything (including data)
docker-compose down -v
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
