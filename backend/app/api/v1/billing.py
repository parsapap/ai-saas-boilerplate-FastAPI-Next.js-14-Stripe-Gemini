from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import stripe
from app.dependencies import get_current_active_user
from app.models.user import User
from app.core.config import settings

router = APIRouter()
stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateCheckoutSessionRequest(BaseModel):
    price_id: str
    success_url: str
    cancel_url: str


@router.post("/create-checkout-session")
async def create_checkout_session(
    request: CreateCheckoutSessionRequest,
    current_user: User = Depends(get_current_active_user)
):
    """Create a Stripe checkout session for subscription"""
    if not current_user.stripe_customer_id:
        raise HTTPException(status_code=400, detail="No Stripe customer ID found")
    
    try:
        checkout_session = stripe.checkout.Session.create(
            customer=current_user.stripe_customer_id,
            payment_method_types=["card"],
            line_items=[{
                "price": request.price_id,
                "quantity": 1,
            }],
            mode="subscription",
            success_url=request.success_url,
            cancel_url=request.cancel_url,
        )
        return {"checkout_url": checkout_session.url}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/customer-portal")
async def create_customer_portal_session(
    return_url: str,
    current_user: User = Depends(get_current_active_user)
):
    """Create a Stripe customer portal session"""
    if not current_user.stripe_customer_id:
        raise HTTPException(status_code=400, detail="No Stripe customer ID found")
    
    try:
        portal_session = stripe.billing_portal.Session.create(
            customer=current_user.stripe_customer_id,
            return_url=return_url,
        )
        return {"portal_url": portal_session.url}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
