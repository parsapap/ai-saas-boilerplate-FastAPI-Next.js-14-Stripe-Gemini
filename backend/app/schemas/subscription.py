from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal
from app.models.subscription import PlanType, SubscriptionStatus


class PlanInfo(BaseModel):
    """Information about available plans"""
    name: str
    type: PlanType
    price: Decimal
    currency: str
    interval: str
    features: list[str]
    stripe_price_id: Optional[str] = None


class CheckoutRequest(BaseModel):
    plan_type: PlanType
    success_url: str
    cancel_url: str


class CheckoutResponse(BaseModel):
    checkout_url: str
    session_id: str


class PortalRequest(BaseModel):
    return_url: str


class PortalResponse(BaseModel):
    portal_url: str


class SubscriptionResponse(BaseModel):
    id: int
    organization_id: int
    plan_type: PlanType
    status: SubscriptionStatus
    amount: Optional[Decimal] = None
    currency: str
    current_period_start: Optional[datetime] = None
    current_period_end: Optional[datetime] = None
    cancel_at_period_end: bool
    trial_end: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
