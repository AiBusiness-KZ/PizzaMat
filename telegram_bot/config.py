"""
Bot configuration from environment variables
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Bot settings"""

    # Telegram Bot
    BOT_TOKEN: str
    MANAGER_CHANNEL_ID: int  # Channel ID for manager notifications (-1001234567890)
    ADMIN_TELEGRAM_IDS: str = ""  # Comma-separated list of admin Telegram IDs

    # Backend API
    BACKEND_URL: str = "http://backend:8000"
    BACKEND_TIMEOUT: int = 30

    # WebApp
    WEBAPP_URL: str = "http://localhost:5173"

    # n8n Integration
    N8N_URL: str = ""
    N8N_WEBHOOK_SECRET: str = ""

    # Database (same as backend)
    DATABASE_URL: str

    # Bot behavior
    SESSION_TIMEOUT_MINUTES: int = 30
    MAX_FILE_SIZE_MB: int = 10

    # Logging
    LOG_LEVEL: str = "INFO"
    DEBUG: bool = False

    # Rate limiting
    RATE_LIMIT_MESSAGES: int = 20  # Max messages per minute
    RATE_LIMIT_COMMANDS: int = 10  # Max commands per minute

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def admin_ids(self) -> List[int]:
        """Parse admin IDs from comma-separated string"""
        if not self.ADMIN_TELEGRAM_IDS:
            return []
        return [int(id.strip()) for id in self.ADMIN_TELEGRAM_IDS.split(",") if id.strip()]


# Global settings instance
settings = Settings()
