"""
Configuration and Environment Variables
Loads settings from .env file

Author: Vignesh (Backend Developer)
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings"""
    
    # Environment
    ENVIRONMENT: str = "development"
    
    # Database
    DATABASE_URL: str = "mongodb://mongo:27017/cycology"
    DATABASE_NAME: str = "cycology"
    
    # AI Agent
    AGENT_URL: str = "http://agent:8001"
    
    # Redis
    REDIS_URL: str = "redis://redis:6379"
    
    # JWT Settings
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://frontend:3000",
    ]
    
    # App Settings
    APP_NAME: str = "Cycology Agent"
    API_V1_PREFIX: str = "/api/v1"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()


