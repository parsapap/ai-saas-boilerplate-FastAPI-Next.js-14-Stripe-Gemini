from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.dependencies import (
    get_current_active_user,
    get_current_organization,
    require_pro_plan,
    require_team_plan
)
from app.models.user import User
from app.models.organization import Organization

router = APIRouter()


@router.get("/analytics")
async def get_analytics(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    current_org: Organization = Depends(get_current_organization),
    subscription = Depends(require_pro_plan)
):
    """
    Advanced analytics - Requires Pro or Team plan
    
    این feature فقط برای کاربران Pro و Team در دسترس هست
    """
    return {
        "message": "Welcome to advanced analytics!",
        "plan": subscription.plan_type.value,
        "organization": current_org.name,
        "features": [
            "Real-time metrics",
            "Custom dashboards",
            "Export reports",
            "API access"
        ]
    }


@router.get("/white-label")
async def get_white_label_settings(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    current_org: Organization = Depends(get_current_organization),
    subscription = Depends(require_team_plan)
):
    """
    White-label settings - Requires Team plan only
    
    این feature فقط برای کاربران Team در دسترس هست
    """
    return {
        "message": "Welcome to white-label settings!",
        "plan": subscription.plan_type.value,
        "organization": current_org.name,
        "features": [
            "Custom branding",
            "Custom domain",
            "Remove powered by",
            "Custom email templates"
        ]
    }


@router.get("/free-feature")
async def get_free_feature(
    current_user: User = Depends(get_current_active_user),
    current_org: Organization = Depends(get_current_organization)
):
    """
    Free feature - Available for all plans
    
    این feature برای همه plans در دسترس هست
    """
    return {
        "message": "This is a free feature!",
        "organization": current_org.name,
        "available_for": "all plans"
    }
