from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from datetime import datetime
from app.models.subscription import Subscription, PlanType, SubscriptionStatus


async def get_subscription_by_org(db: AsyncSession, org_id: int) -> Optional[Subscription]:
    result = await db.execute(
        select(Subscription).where(Subscription.organization_id == org_id)
    )
    return result.scalar_one_or_none()


async def get_subscription_by_stripe_id(db: AsyncSession, stripe_subscription_id: str) -> Optional[Subscription]:
    result = await db.execute(
        select(Subscription).where(Subscription.stripe_subscription_id == stripe_subscription_id)
    )
    return result.scalar_one_or_none()


async def create_subscription(
    db: AsyncSession,
    org_id: int,
    plan_type: PlanType = PlanType.FREE,
    stripe_customer_id: Optional[str] = None
) -> Subscription:
    """Create a new subscription (default: Free plan)"""
    subscription = Subscription(
        organization_id=org_id,
        plan_type=plan_type,
        status=SubscriptionStatus.ACTIVE,
        stripe_customer_id=stripe_customer_id
    )
    db.add(subscription)
    await db.commit()
    await db.refresh(subscription)
    return subscription


async def update_subscription_from_stripe(
    db: AsyncSession,
    subscription: Subscription,
    stripe_subscription: dict
) -> Subscription:
    """Update subscription from Stripe webhook data"""
    from app.core.stripe_config import get_plan_from_price_id
    import logging
    logger = logging.getLogger(__name__)
    
    subscription.stripe_subscription_id = stripe_subscription.get("id")
    subscription.status = SubscriptionStatus(stripe_subscription.get("status"))
    
    # Get price ID and update plan type
    price_id = stripe_subscription["items"]["data"][0]["price"]["id"]
    subscription.stripe_price_id = price_id
    
    logger.info(f"Updating subscription with price_id: {price_id}")
    
    # Map price ID to plan type
    plan_type = get_plan_from_price_id(price_id)
    if plan_type:
        logger.info(f"Mapped price_id {price_id} to plan_type: {plan_type}")
        subscription.plan_type = plan_type
    else:
        logger.warning(f"Could not map price_id {price_id} to a plan_type. Current plan: {subscription.plan_type}")
    
    subscription.amount = stripe_subscription["items"]["data"][0]["price"]["unit_amount"] / 100
    subscription.currency = stripe_subscription["items"]["data"][0]["price"]["currency"]
    subscription.current_period_start = datetime.fromtimestamp(stripe_subscription.get("current_period_start"))
    subscription.current_period_end = datetime.fromtimestamp(stripe_subscription.get("current_period_end"))
    subscription.cancel_at_period_end = stripe_subscription.get("cancel_at_period_end", False)
    
    if stripe_subscription.get("canceled_at"):
        subscription.canceled_at = datetime.fromtimestamp(stripe_subscription["canceled_at"])
    
    if stripe_subscription.get("trial_end"):
        subscription.trial_end = datetime.fromtimestamp(stripe_subscription["trial_end"])
    
    await db.commit()
    await db.refresh(subscription)
    return subscription


async def update_subscription_plan(
    db: AsyncSession,
    subscription: Subscription,
    plan_type: PlanType
) -> Subscription:
    """Update subscription plan type"""
    subscription.plan_type = plan_type
    await db.commit()
    await db.refresh(subscription)
    return subscription


async def cancel_subscription(
    db: AsyncSession,
    subscription: Subscription
) -> Subscription:
    """Mark subscription as canceled"""
    subscription.status = SubscriptionStatus.CANCELED
    subscription.canceled_at = datetime.utcnow()
    await db.commit()
    await db.refresh(subscription)
    return subscription
