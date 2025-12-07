from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
import stripe
from typing import List
from app.database import get_db
from app.dependencies import get_current_active_user, get_current_organization
from app.models.user import User
from app.models.organization import Organization
from app.models.subscription import PlanType
from app.schemas.subscription import (
    PlanInfo,
    CheckoutRequest,
    CheckoutResponse,
    PortalRequest,
    PortalResponse,
    SubscriptionResponse
)
from app.crud import subscription as crud_subscription
from app.core.config import settings
from app.core.stripe_config import STRIPE_PRICES, PLAN_CONFIGS
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize Stripe lazily to avoid import errors
def init_stripe():
    if not hasattr(init_stripe, '_initialized'):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        init_stripe._initialized = True


@router.get("/plans", response_model=List[PlanInfo])
async def get_available_plans():
    """Get all available subscription plans"""
    init_stripe()
    plans = []
    for plan_type, config in PLAN_CONFIGS.items():
        plans.append(PlanInfo(
            name=config["name"],
            type=plan_type,
            price=config["price"],
            currency=config["currency"],
            interval=config["interval"],
            features=config["features"],
            stripe_price_id=STRIPE_PRICES.get(plan_type)
        ))
    return plans


@router.get("/subscription", response_model=SubscriptionResponse)
async def get_current_subscription(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    current_org: Organization = Depends(get_current_organization)
):
    """Get current organization's subscription"""
    subscription = await crud_subscription.get_subscription_by_org(db, current_org.id)
    
    if not subscription:
        # Create free subscription if doesn't exist
        subscription = await crud_subscription.create_subscription(
            db, current_org.id, PlanType.FREE, current_org.stripe_customer_id
        )
    
    return subscription


@router.post("/checkout", response_model=CheckoutResponse)
async def create_checkout_session(
    request: CheckoutRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    current_org: Organization = Depends(get_current_organization)
):
    """Create Stripe checkout session for subscription"""
    init_stripe()
    
    # Validate plan
    if request.plan_type == PlanType.FREE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot create checkout for free plan"
        )
    
    stripe_price_id = STRIPE_PRICES.get(request.plan_type)
    if not stripe_price_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid plan type"
        )
    
    # Get or create Stripe customer
    if not current_org.stripe_customer_id:
        try:
            customer = stripe.Customer.create(
                email=current_user.email,
                name=current_org.name,
                metadata={
                    "organization_id": current_org.id,
                    "organization_slug": current_org.slug
                }
            )
            current_org.stripe_customer_id = customer.id
            await db.commit()
        except Exception as e:
            logger.error(f"Failed to create Stripe customer: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create customer"
            )
    
    # Create checkout session
    try:
        checkout_session = stripe.checkout.Session.create(
            customer=current_org.stripe_customer_id,
            payment_method_types=["card"],
            line_items=[{
                "price": stripe_price_id,
                "quantity": 1,
            }],
            mode="subscription",
            success_url=request.success_url,
            cancel_url=request.cancel_url,
            metadata={
                "organization_id": current_org.id,
                "plan_type": request.plan_type.value
            }
        )
        
        return CheckoutResponse(
            checkout_url=checkout_session.url,
            session_id=checkout_session.id
        )
    except Exception as e:
        logger.error(f"Failed to create checkout session: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/portal", response_model=PortalResponse)
async def create_customer_portal_session(
    request: PortalRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    current_org: Organization = Depends(get_current_organization)
):
    """Create Stripe customer portal session"""
    init_stripe()
    if not current_org.stripe_customer_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No Stripe customer found"
        )
    
    try:
        portal_session = stripe.billing_portal.Session.create(
            customer=current_org.stripe_customer_id,
            return_url=request.return_url,
        )
        
        return PortalResponse(portal_url=portal_session.url)
    except Exception as e:
        logger.error(f"Failed to create portal session: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/webhook/stripe")
async def stripe_webhook(request: Request, db: AsyncSession = Depends(get_db)):
    """Handle Stripe webhooks"""
    init_stripe()
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        logger.error("Invalid payload")
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        logger.error("Invalid signature")
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    # Handle the event
    event_type = event["type"]
    data = event["data"]["object"]
    
    logger.info(f"Received Stripe webhook: {event_type}")
    
    try:
        if event_type == "checkout.session.completed":
            await handle_checkout_completed(db, data)
        
        elif event_type == "customer.subscription.updated":
            await handle_subscription_updated(db, data)
        
        elif event_type == "customer.subscription.deleted":
            await handle_subscription_deleted(db, data)
        
        elif event_type == "invoice.paid":
            await handle_invoice_paid(db, data)
        
        elif event_type == "invoice.payment_failed":
            await handle_invoice_payment_failed(db, data)
        
        else:
            logger.info(f"Unhandled event type: {event_type}")
    
    except Exception as e:
        logger.error(f"Error handling webhook {event_type}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
    return {"status": "success"}


async def handle_checkout_completed(db: AsyncSession, session: dict):
    """Handle successful checkout"""
    org_id = int(session["metadata"]["organization_id"])
    plan_type = PlanType(session["metadata"]["plan_type"])
    
    # Get subscription from Stripe
    stripe_subscription_id = session["subscription"]
    stripe_subscription = stripe.Subscription.retrieve(stripe_subscription_id)
    
    # Get or create subscription record
    subscription = await crud_subscription.get_subscription_by_org(db, org_id)
    if not subscription:
        subscription = await crud_subscription.create_subscription(
            db, org_id, plan_type, session["customer"]
        )
    
    # Update subscription from Stripe data (this will set the correct plan based on price_id)
    await crud_subscription.update_subscription_from_stripe(db, subscription, stripe_subscription)
    
    logger.info(f"Checkout completed for org {org_id}, plan: {subscription.plan_type}")


async def handle_subscription_updated(db: AsyncSession, subscription_data: dict):
    """Handle subscription update"""
    subscription = await crud_subscription.get_subscription_by_stripe_id(
        db, subscription_data["id"]
    )
    
    if subscription:
        await crud_subscription.update_subscription_from_stripe(db, subscription, subscription_data)
        logger.info(f"Subscription updated: {subscription_data['id']}")


async def handle_subscription_deleted(db: AsyncSession, subscription_data: dict):
    """Handle subscription cancellation"""
    subscription = await crud_subscription.get_subscription_by_stripe_id(
        db, subscription_data["id"]
    )
    
    if subscription:
        # Downgrade to free plan
        subscription.plan_type = PlanType.FREE
        await crud_subscription.cancel_subscription(db, subscription)
        logger.info(f"Subscription canceled: {subscription_data['id']}")


async def handle_invoice_paid(db: AsyncSession, invoice: dict):
    """Handle successful payment"""
    subscription_id = invoice.get("subscription")
    if subscription_id:
        subscription = await crud_subscription.get_subscription_by_stripe_id(db, subscription_id)
        if subscription:
            logger.info(f"Invoice paid for subscription: {subscription_id}")


async def handle_invoice_payment_failed(db: AsyncSession, invoice: dict):
    """Handle failed payment"""
    subscription_id = invoice.get("subscription")
    if subscription_id:
        subscription = await crud_subscription.get_subscription_by_stripe_id(db, subscription_id)
        if subscription:
            from app.models.subscription import SubscriptionStatus
            subscription.status = SubscriptionStatus.PAST_DUE
            await db.commit()
            logger.warning(f"Payment failed for subscription: {subscription_id}")
