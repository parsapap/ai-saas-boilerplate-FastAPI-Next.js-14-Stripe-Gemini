from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import date


class Message(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str


class ChatRequest(BaseModel):
    messages: List[Message] = Field(..., min_length=1)
    model: Literal[
        "gemini-2.0-flash",
        "gemini-1.5-flash",
        "gemini-1.5-pro",
        "claude-3-haiku",
        "gpt-4o-mini"
    ] = "gemini-2.0-flash"
    temperature: Optional[float] = Field(default=0.7, ge=0, le=2)
    max_tokens: Optional[int] = Field(default=1024, ge=1, le=8192)
    stream: bool = False


class ChatResponse(BaseModel):
    message: str
    model: str
    usage: dict
    finish_reason: str


class UsageStats(BaseModel):
    organization_id: int
    date: date
    model: str
    message_count: int
    input_tokens: int
    output_tokens: int
    total_tokens: int
    estimated_cost: int
    
    class Config:
        from_attributes = True


class UsageSummary(BaseModel):
    """Monthly usage summary"""
    total_messages: int
    total_tokens: int
    messages_limit: Optional[int]
    tokens_limit: Optional[int]
    usage_percentage: float
    models_breakdown: dict
