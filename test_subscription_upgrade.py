#!/usr/bin/env python3
"""
Test script to manually upgrade a user's subscription
Usage: python test_subscription_upgrade.py <email> <plan_type>
Example: python test_subscription_upgrade.py parsa@gmail.com team
"""

import sys
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

# Add backend to path
sys.path.insert(0, 'backend')

from app.models.user import User
from app.models.organization import Organization, Membership
from app.models.subscription import Subscription, PlanType, SubscriptionStatus
from app.core.config import settings


async def upgrade_subscription(email: str, plan_type_str: str):
    """Upgrade a user's subscription"""
    
    # Validate plan type
    try:
        plan_type = PlanType(plan_type_str.lower())
    except ValueError:
        print(f"❌ Invalid plan type: {plan_type_str}")
        print(f"   Valid options: free, pro, team")
        return
    
    # Create database connection
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as db:
        # Find user
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        
        if not user:
            print(f"❌ User not found: {email}")
            return
        
        print(f"✅ Found user: {user.email} (ID: {user.id})")
        
        # Find user's organization
        result = await db.execute(
            select(Organization)
            .join(Membership)
            .where(Membership.user_id == user.id)
        )
        org = result.scalar_one_or_none()
        
        if not org:
            print(f"❌ No organization found for user")
            return
        
        print(f"✅ Found organization: {org.name} (ID: {org.id})")
        
        # Find or create subscription
        result = await db.execute(
            select(Subscription).where(Subscription.organization_id == org.id)
        )
        subscription = result.scalar_one_or_none()
        
        if not subscription:
            print(f"📝 Creating new subscription...")
            subscription = Subscription(
                organization_id=org.id,
                plan_type=plan_type,
                status=SubscriptionStatus.ACTIVE
            )
            db.add(subscription)
        else:
            print(f"📝 Current plan: {subscription.plan_type.value}")
            subscription.plan_type = plan_type
            subscription.status = SubscriptionStatus.ACTIVE
        
        await db.commit()
        await db.refresh(subscription)
        
        print(f"✅ Subscription updated!")
        print(f"   Organization: {org.name}")
        print(f"   Plan: {subscription.plan_type.value}")
        print(f"   Status: {subscription.status.value}")
        print(f"\n🎉 User {email} is now on the {plan_type.value.upper()} plan!")


async def show_user_info(email: str):
    """Show user's current subscription info"""
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as db:
        # Find user
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        
        if not user:
            print(f"❌ User not found: {email}")
            return
        
        print(f"\n👤 User: {user.email}")
        print(f"   ID: {user.id}")
        print(f"   Name: {user.full_name}")
        
        # Find organization
        result = await db.execute(
            select(Organization)
            .join(Membership)
            .where(Membership.user_id == user.id)
        )
        org = result.scalar_one_or_none()
        
        if org:
            print(f"\n🏢 Organization: {org.name}")
            print(f"   ID: {org.id}")
            print(f"   Slug: {org.slug}")
            
            # Find subscription
            result = await db.execute(
                select(Subscription).where(Subscription.organization_id == org.id)
            )
            subscription = result.scalar_one_or_none()
            
            if subscription:
                print(f"\n💳 Subscription:")
                print(f"   Plan: {subscription.plan_type.value}")
                print(f"   Status: {subscription.status.value}")
                if subscription.amount:
                    print(f"   Amount: ${subscription.amount}/{subscription.currency}")
            else:
                print(f"\n⚠️  No subscription found")
        else:
            print(f"\n⚠️  No organization found")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Show user info:    python test_subscription_upgrade.py <email>")
        print("  Upgrade plan:      python test_subscription_upgrade.py <email> <plan_type>")
        print("\nExamples:")
        print("  python test_subscription_upgrade.py parsa@gmail.com")
        print("  python test_subscription_upgrade.py parsa@gmail.com team")
        print("  python test_subscription_upgrade.py parsa@gmail.com pro")
        sys.exit(1)
    
    email = sys.argv[1]
    
    if len(sys.argv) == 2:
        # Show info only
        asyncio.run(show_user_info(email))
    else:
        # Upgrade subscription
        plan_type = sys.argv[2]
        asyncio.run(upgrade_subscription(email, plan_type))
