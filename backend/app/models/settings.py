"""
Settings model
Site configuration settings
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON
from sqlalchemy.sql import func

from app.database import Base


class SiteSettings(Base):
    """Site settings model - singleton table with id=1"""
    
    __tablename__ = "site_settings"
    
    id = Column(Integer, primary_key=True, default=1)
    
    # Site info
    site_name = Column(String(100), default="PizzaMat")
    site_logo = Column(String(500), nullable=True)
    site_description = Column(Text, nullable=True)
    
    # Contact info
    phone = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    address = Column(Text, nullable=True)
    
    # Telegram settings
    bot_token = Column(String(200), nullable=True)
    manager_channel_id = Column(String(50), nullable=True)
    admin_telegram_ids = Column(Text, nullable=True)  # Comma-separated
    
    # OpenAI settings
    openai_api_key = Column(String(200), nullable=True)
    
    # n8n settings
    n8n_url = Column(String(200), nullable=True)
    n8n_webhook_secret = Column(String(200), nullable=True)
    
    # Additional settings (JSON)
    extra_settings = Column(JSON, nullable=True)
    
    # Metadata
    is_active = Column(Boolean, default=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<SiteSettings(id={self.id}, site_name='{self.site_name}')>"
