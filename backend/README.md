# 🟢 Psychology Backend - FastAPI

**Owner**: Vignesh (Backend Developer)

## 🚀 Quick Start

### Using Docker (Recommended)
```bash
# From project root
cd "Psychology Agent"
docker-compose up --build backend mongo redis

# Backend available at:
# - http://localhost:8000
# - http://localhost:8000/docs (API docs)
```

### Local Development
```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux/Mac
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## 📁 Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI entry point
│   ├── config.py            # Configuration
│   ├── api/v1/              # API routes
│   │   ├── auth.py          # Authentication
│   │   ├── chat.py          # Chat & WebSocket
│   │   ├── users.py         # User management
│   │   └── appointments.py  # Appointments (Phase 2)
│   ├── models/              # Database models
│   ├── schemas/             # Pydantic schemas
│   ├── services/            # Business logic
│   └── utils/               # Utilities
└── requirements.txt
```

## 📚 Documentation

See **[BACKEND_GUIDE.md](./BACKEND_GUIDE.md)** for complete documentation:
- API endpoints
- Testing guide
- WebSocket usage
- Troubleshooting
- Git workflow

## ✅ What's Implemented

✅ User Authentication (JWT)  
✅ Anonymous User Support  
✅ MongoDB Integration  
✅ WebSocket Chat  
✅ AI Agent Bridge  
✅ Session Management  
✅ Message History  
✅ API Documentation (auto-generated)  

## 🧪 Test the API

Visit http://localhost:8000/docs for interactive API testing!

## 🔑 Environment Variables

Required environment variables (set in docker-compose.yml or .env):

```env
DATABASE_URL=mongodb://mongo:27017/psychology
AGENT_URL=http://agent:8001
REDIS_URL=redis://redis:6379
SECRET_KEY=your-secret-key-here
```

## 📞 API Endpoints

- **Auth**: `/api/v1/auth/*` - Register, login, anonymous
- **Users**: `/api/v1/users/*` - Profile management
- **Chat**: `/api/v1/chat/*` - Sessions, messages, WebSocket
- **Appointments**: `/api/v1/appointments/*` - Phase 2 (placeholder)

---

**Your backend is ready to go! 🚀**
