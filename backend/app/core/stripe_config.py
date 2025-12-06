from app.models.subscription import PlanType
from decimal import Decimal
from typing import Optional

# Stripe Price IDs (replace with your actual IDs from Stripe Dashboard)
STRIPE_PRICES = {
    PlanType.FREE: None,  # Free plan has no Stripe price
    PlanType.PRO: "price_1SaL4MJQFLCmojG3bVa6HbGt",  # Pro Plan - $29/month
    PlanType.TEAM: "price_1SaL8SJQFLCmojG3vspXn8TA",  # Team Plan - $99/month
}

# Reverse mapping: Price ID to Plan Type
PRICE_TO_PLAN = {v: k for k, v in STRIPE_PRICES.items() if v is not None}

# Plan configurations
PLAN_CONFIGS = {
    PlanType.FREE: {
        "name": "Free",
        "price": Decimal("0"),
        "currency": "usd",
        "interval": "month",
        "features": [
            "1 organization",
            "5 team members",
            "Basic features",
            "Community support"
        ]
    },
    PlanType.PRO: {
        "name": "Pro",
        "price": Decimal("29"),
        "currency": "usd",
        "interval": "month",
        "features": [
            "3 organizations",
            "20 team members",
            "Advanced features",
            "Priority support",
            "API access",
            "Custom integrations"
        ]
    },
    PlanType.TEAM: {
        "name": "Team",
        "price": Decimal("99"),
        "currency": "usd",
        "interval": "month",
        "features": [
            "Unlimited organizations",
            "Unlimited team members",
            "All Pro features",
            "24/7 support",
            "Advanced analytics",
            "Custom branding",
            "SLA guarantee"
        ]
    }
}

# Plan limits
PLAN_LIMITS = {
    PlanType.FREE: {
        "max_organizations": 1,
        "max_members_per_org": 5,
        "max_api_keys": 2,
        "api_rate_limit": 100,  # requests per hour
    },
    PlanType.PRO: {
        "max_organizations": 3,
        "max_members_per_org": 20,
        "max_api_keys": 10,
        "api_rate_limit": 1000,
    },
    PlanType.TEAM: {
        "max_organizations": None,  # Unlimited
        "max_members_per_org": None,
        "max_api_keys": None,
        "api_rate_limit": 10000,
    }
}


def get_plan_limit(plan_type: PlanType, limit_name: str) -> int | None:
    """Get a specific limit for a plan"""
    return PLAN_LIMITS.get(plan_type, {}).get(limit_name)


def get_plan_from_price_id(price_id: str) -> Optional[PlanType]:
    """Get plan type from Stripe price ID"""
    return PRICE_TO_PLAN.get(price_id)
