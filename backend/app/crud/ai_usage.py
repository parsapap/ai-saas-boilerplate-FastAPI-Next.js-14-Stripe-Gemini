from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from datetime import date, datetime, timedelta
from typing import List, Optional
from app.models.ai_usage import AIUsage, AIRequest


async def get_or_create_daily_usage(
    db: AsyncSession,
    org_id: int,
    model: str,
    usage_date: date = None
) -> AIUsage:
    """Get or create daily usage record"""
    if usage_date is None:
        usage_date = date.today()
    
    result = await db.execute(
        select(AIUsage).where(
            and_(
                AIUsage.organization_id == org_id,
                AIUsage.model == model,
                AIUsage.date == usage_date
            )
        )
    )
    usage = result.scalar_one_or_none()
    
    if not usage:
        usage = AIUsage(
            organization_id=org_id,
            model=model,
            date=usage_date
        )
        db.add(usage)
        await db.commit()
        await db.refresh(usage)
    
    return usage


async def update_usage(
    db: AsyncSession,
    org_id: int,
    model: str,
    input_tokens: int,
    output_tokens: int,
    cost_cents: int
):
    """Update daily usage"""
    usage = await get_or_create_daily_usage(db, org_id, model)
    
    usage.message_count += 1
    usage.input_tokens += input_tokens
    usage.output_tokens += output_tokens
    usage.total_tokens += (input_tokens + output_tokens)
    usage.estimated_cost += cost_cents
    
    await db.commit()
    await db.refresh(usage)
    return usage


async def log_request(
    db: AsyncSession,
    org_id: int,
    user_id: Optional[int],
    model: str,
    input_tokens: int,
    output_tokens: int,
    duration_ms: int,
    status: str = "success",
    error_message: Optional[str] = None
):
    """Log individual AI request"""
    request = AIRequest(
        organization_id=org_id,
        user_id=user_id,
        model=model,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        total_tokens=input_tokens + output_tokens,
        duration_ms=duration_ms,
        status=status,
        error_message=error_message
    )
    db.add(request)
    await db.commit()
    return request


async def get_monthly_usage(
    db: AsyncSession,
    org_id: int,
    year: int = None,
    month: int = None
) -> List[AIUsage]:
    """Get monthly usage"""
    if year is None or month is None:
        now = datetime.utcnow()
        year = now.year
        month = now.month
    
    start_date = date(year, month, 1)
    if month == 12:
        end_date = date(year + 1, 1, 1)
    else:
        end_date = date(year, month + 1, 1)
    
    result = await db.execute(
        select(AIUsage).where(
            and_(
                AIUsage.organization_id == org_id,
                AIUsage.date >= start_date,
                AIUsage.date < end_date
            )
        )
    )
    return result.scalars().all()


async def get_usage_summary(
    db: AsyncSession,
    org_id: int
) -> dict:
    """Get usage summary for current month"""
    usage_records = await get_monthly_usage(db, org_id)
    
    total_messages = sum(u.message_count for u in usage_records)
    total_tokens = sum(u.total_tokens for u in usage_records)
    total_cost = sum(u.estimated_cost for u in usage_records)
    
    # Breakdown by model
    models_breakdown = {}
    for usage in usage_records:
        if usage.model not in models_breakdown:
            models_breakdown[usage.model] = {
                "messages": 0,
                "tokens": 0,
                "cost": 0
            }
        models_breakdown[usage.model]["messages"] += usage.message_count
        models_breakdown[usage.model]["tokens"] += usage.total_tokens
        models_breakdown[usage.model]["cost"] += usage.estimated_cost
    
    return {
        "total_messages": total_messages,
        "total_tokens": total_tokens,
        "total_cost_cents": total_cost,
        "models_breakdown": models_breakdown
    }
