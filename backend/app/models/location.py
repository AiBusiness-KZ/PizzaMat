"""
Location models
Cities and pickup locations
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class City(Base):
    """City model"""
    
    __tablename__ = "cities"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    locations = relationship("Location", back_populates="city", cascade="all, delete-orphan")
    users = relationship("User", back_populates="city")
    
    def __repr__(self):
        return f"<City(id={self.id}, name='{self.name}')>"


class Location(Base):
    """Pickup location model"""
    
    __tablename__ = "locations"
    
    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("cities.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    address = Column(Text, nullable=False)
    working_hours = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    city = relationship("City", back_populates="locations")
    location_products = relationship("LocationProduct", back_populates="location", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="location")
    
    def __repr__(self):
        return f"<Location(id={self.id}, name='{self.name}', city_id={self.city_id})>"
