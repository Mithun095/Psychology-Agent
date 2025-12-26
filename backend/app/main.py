"""
Cycology Agent - Backend API
FastAPI application entry point

Author: Vignesh (Backend Developer)
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.api.v1 import auth, chat, users, appointments
from app.utils.database import connect_to_mongo, close_mongo_connection


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    print("🚀 Starting Cycology Backend...")
    await connect_to_mongo()
    print("✅ Connected to MongoDB")
    yield
    # Shutdown
    print("👋 Shutting down Cycology Backend...")
    await close_mongo_connection()
    print("✅ Closed MongoDB connection")


# Initialize FastAPI app
app = FastAPI(
    title="Cycology Agent API",
    description="Mental Health Support Platform - Backend API",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/")
async def root():
    """Root endpoint - Health check"""
    return {
        "status": "healthy",
        "service": "Cycology Backend API",
        "version": "1.0.0",
        "message": "Welcome to Cycology Agent API - Mental Health Support Platform"
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "database": "connected",
        "agent_url": settings.AGENT_URL
    }


# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(chat.router, prefix="/api/v1/chat", tags=["Chat"])
app.include_router(appointments.router, prefix="/api/v1/appointments", tags=["Appointments"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )


