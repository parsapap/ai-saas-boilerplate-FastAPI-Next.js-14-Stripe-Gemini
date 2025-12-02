from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class AIUsage(Base):
    """Track AI usage per organization per day"""
    __tablename__ = "ai_usage"
    
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False)
    
    # Date tracking
    date = Column(Date, nullable=False, index=True)
    
    # Model info
    model = Column(String, nullable=False)  # gemini-1.5-flash, gpt-4o-mini, etc.
    
    # Usage metrics
    message_count = Column(Integer, default=0)
    input_tokens = Column(BigInteger, default=0)
    output_tokens = Column(BigInteger, default=0)
    total_tokens = Column(BigInteger, default=0)
    
    # Cost tracking (optional)
    estimated_cost = Column(Integer, default=0)  # in cents
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    organization = relationship("Organization")


class AIRequest(Base):
    """Individual AI request log"""
    __tablename__ = "ai_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Request details
    model = Column(String, nullable=False)
    prompt_length = Column(Integer, nullable=True)
    response_length = Column(Integer, nullable=True)
    
    # Tokens
    input_tokens = Column(Integer, nullable=True)
    output_tokens = Column(Integer, nullable=True)
    total_tokens = Column(Integer, nullable=True)
    
    # Performance
    duration_ms = Column(Integer, nullable=True)  # milliseconds
    status = Column(String, nullable=False)  # success, error, timeout
    error_message = Column(String, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    organization = relationship("Organization")
    user = relationship("User")
