from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ApiKeyCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    expires_at: Optional[datetime] = None


class ApiKeyResponse(BaseModel):
    id: int
    name: str
    key_prefix: str
    organization_id: int
    created_by: int
    last_used_at: Optional[datetime] = None
    is_active: bool
    created_at: datetime
    expires_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ApiKeyWithSecret(ApiKeyResponse):
    """Only returned once when creating a new API key"""
    key: str  # Full key: sk-xxx...
