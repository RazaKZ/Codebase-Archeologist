"""
Application settings and configuration
"""
from pydantic_settings import BaseSettings
from typing import List, Union
from pydantic import field_validator

class Settings(BaseSettings):
    # API Keys (use environment variables)
    SNYK_API_KEY: str = ""
    GEMINI_API_KEY: str = ""
    
    # Database
    DATABASE_URL: str = "sqlite:///./codebase_archeologist.db"
    
    # CORS
    # For production, set CORS_ORIGINS environment variable in Railway
    # Example: CORS_ORIGINS=https://codebase-archeologist.vercel.app,http://localhost:5173
    CORS_ORIGINS: Union[str, List[str]] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "https://codebase-archeologist.vercel.app"
    ]
    
    @field_validator('CORS_ORIGINS', mode='before')
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            # Split comma-separated string and strip whitespace
            return [origin.strip() for origin in v.split(',') if origin.strip()]
        return v
    
    # Analysis settings
    MAX_REPO_SIZE_MB: int = 100
    ANALYSIS_TIMEOUT_SECONDS: int = 300
    CACHE_TTL_SECONDS: int = 3600
    
    # LLM settings
    LLM_MODEL: str = "gemini-1.5-flash"  # Updated to latest model
    LLM_TEMPERATURE: float = 0.3
    LLM_MAX_TOKENS: int = 2000
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

