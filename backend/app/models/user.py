"""
User model
"""

from sqlalchemy import Column, Integer, BigInteger, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class User(Base):
    """User model - registered Telegram users"""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False, index=True)
    phone = Column(String(20), nullable=False, index=True)
    full_name = Column(String(255), nullable=False)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=True)
    language = Column(String(5), default="uk")  # uk, en, ru
    is_active = Column(Boolean, default=True, index=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    city = relationship("City", back_populates="users")
    orders = relationship("Order", foreign_keys="Order.user_id", back_populates="user")
    
    def __repr__(self):
        return f"<User(id={self.id}, telegram_id={self.telegram_id}, name='{self.full_name}')>"
