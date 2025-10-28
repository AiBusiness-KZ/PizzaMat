"""
Application configuration
Loads settings from environment variables
"""

from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
import json


class Settings(BaseSettings):
    """Application settings loaded from .env file"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://pizzamat:pizzamat_dev_password@localhost:5432/pizzamatif"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # JWT
    JWT_SECRET: str = "dev_jwt_secret_change_in_production_min_32_chars"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_HOURS: int = 24
    
    # Telegram (optional for backend, required for bot)
    BOT_TOKEN: Optional[str] = None
    TELEGRAM_WEBHOOK_SECRET: Optional[str] = None
    MANAGER_CHANNEL_ID: Optional[int] = None
    ADMIN_TELEGRAM_IDS: Optional[str] = None
    
    # OpenAI (for n8n workflow)
    OPENAI_API_KEY: Optional[str] = None
    
    # n8n
    N8N_URL: Optional[str] = None
    N8N_WEBHOOK_SECRET: Optional[str] = None
    N8N_WEBHOOK_URL: Optional[str] = None
    
    # Application
    DEBUG: bool = True
    ALLOWED_ORIGINS: str = '["http://localhost:3000","http://localhost:5173"]'
    WEBAPP_URL: str = "http://localhost:5173"
    
    # File Upload
    MAX_FILE_SIZE: int = 10485760  # 10 MB
    UPLOAD_DIR: str = "./uploads"
    ALLOWED_IMAGE_TYPES: List[str] = ["image/jpeg", "image/png", "image/webp"]
    
    # Localization
    DEFAULT_LANGUAGE: str = "uk"  # Ukrainian
    SUPPORTED_LANGUAGES: List[str] = ["uk", "en", "ru"]
    
    @property
    def admin_ids(self) -> List[int]:
        """Parse admin telegram IDs from comma-separated string"""
        if not self.ADMIN_TELEGRAM_IDS:
            return []
        return [int(id.strip()) for id in self.ADMIN_TELEGRAM_IDS.split(",") if id.strip()]
    
    @property
    def origins(self) -> List[str]:
        """Parse ALLOWED_ORIGINS from JSON string"""
        try:
            return json.loads(self.ALLOWED_ORIGINS)
        except:
            return ["http://localhost:3000", "http://localhost:5173"]


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


# Global settings instance
settings = get_settings()
