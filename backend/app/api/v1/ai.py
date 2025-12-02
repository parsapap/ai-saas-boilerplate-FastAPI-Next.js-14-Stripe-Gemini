from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
import time
from app.database import get_db
from app.dependencies import get_current_active_user, get_current_organization
from app.models.user import User
from app.models.organization import Organization
from app.schemas.ai import ChatRequest, ChatResponse, UsageSummary
from app.services.ai_service import AIService
from app.crud import ai_usage as crud_ai_usage
from app.crud import subscription as crud_subscription
from app.core.ai_config import AI_LIMITS, calculate_cost, get_ai_limit
from app.core.rate_limiter import RateLimiter
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


async def check_ai_limits(
    db: AsyncSession,
    org: Organization,
    model: str,
    max_tokens: int
):
    """Check if organization can make AI request"""
    # Get subscription
    subscription = await crud_subscription.get_subscription_by_org(db, org.id)
    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="No active subscription"
        )
    
    plan_type = subscription.plan_type
    
    # Check if model is allowed
    allowed_models = get_ai_limit(plan_type, "allowed_models")
    if model not in allowed_models:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Model {model} not available in your plan. Upgrade to access."
        )
    
    # Check max tokens per request
    max_tokens_limit = get_ai_limit(plan_type, "max_tokens_per_request")
    if max_tokens > max_tokens_limit:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Max tokens per request: {max_tokens_limit}"
        )
    
    # Check rate limit (per minute)
    rate_limit = get_ai_limit(plan_type, "rate_limit_per_minute")
    rate_key = f"ai_rate:{org.id}:minute"
    allowed, current, remaining = RateLimiter.check_rate_limit(rate_key, rate_limit, 60)
    
    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded. Max {rate_limit} requests per minute.",
            headers={"X-RateLimit-Remaining": "0"}
        )
    
    # Check monthly limits
    messages_limit = get_ai_limit(plan_type, "messages_per_month")
    tokens_limit = get_ai_limit(plan_type, "tokens_per_month")
    
    allowed, usage_info = RateLimiter.check_monthly_limit(
        org.id, messages_limit, tokens_limit
    )
    
    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail=f"Monthly limit exceeded. Upgrade your plan to continue.",
            headers={
                "X-Usage-Messages": str(usage_info["current_messages"]),
                "X-Usage-Tokens": str(usage_info["current_tokens"])
            }
        )
    
    return {
        "rate_limit_remaining": remaining,
        "usage_info": usage_info
    }


@router.post("/chat", response_model=ChatResponse)
async def chat_completion(
    request: ChatRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    current_org: Organization = Depends(get_current_organization)
):
    """
    AI Chat Completion
    
    Send messages to AI models and get responses.
    Supports: Gemini 1.5 Flash, Gemini 1.5 Pro, Claude 3 Haiku, GPT-4o Mini
    
    Rate limits apply based on your plan:
    - Free: 50 messages/month, 5 req/min
    - Pro: 10,000 messages/month, 60 req/min
    - Team: Unlimited, 300 req/min
    """
    # Check limits
    limits_info = await check_ai_limits(
        db, current_org, request.model, request.max_tokens
    )
    
    try:
        # Get AI response
        result = await AIService.chat_completion(
            messages=request.messages,
            model=request.model,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
        
        # Update usage
        input_tokens = result["usage"]["input_tokens"]
        output_tokens = result["usage"]["output_tokens"]
        total_tokens = result["usage"]["total_tokens"]
        
        # Calculate cost
        cost_cents = calculate_cost(request.model, input_tokens, output_tokens)
        
        # Update Redis counters
        RateLimiter.increment_monthly_usage(
            current_org.id,
            messages=1,
            tokens=total_tokens
        )
        
        # Update database usage
        await crud_ai_usage.update_usage(
            db, current_org.id, request.model,
            input_tokens, output_tokens, cost_cents
        )
        
        # Log request
        await crud_ai_usage.log_request(
            db, current_org.id, current_user.id, request.model,
            input_tokens, output_tokens, result["duration_ms"],
            status="success"
        )
        
        return ChatResponse(
            message=result["message"],
            model=request.model,
            usage=result["usage"],
            finish_reason=result["finish_reason"]
        )
    
    except Exception as e:
        logger.error(f"AI request failed: {e}")
        
        # Log failed request
        await crud_ai_usage.log_request(
            db, current_org.id, current_user.id, request.model,
            0, 0, 0, status="error", error_message=str(e)
        )
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI request failed: {str(e)}"
        )


@router.post("/chat/stream")
async def chat_completion_stream(
    request: ChatRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    current_org: Organization = Depends(get_current_organization)
):
    """
    AI Chat Completion with Streaming
    
    Stream AI responses in real-time using Server-Sent Events (SSE).
    """
    # Check limits
    await check_ai_limits(db, current_org, request.model, request.max_tokens)
    
    async def generate():
        try:
            start_time = time.time()
            full_response = ""
            
            async for chunk in AIService.chat_completion_stream(
                messages=request.messages,
                model=request.model,
                temperature=request.temperature,
                max_tokens=request.max_tokens
            ):
                full_response += chunk
                yield f"data: {chunk}\n\n"
            
            # Send done signal
            yield "data: [DONE]\n\n"
            
            # Update usage (approximate)
            duration_ms = int((time.time() - start_time) * 1000)
            input_tokens = sum(len(m.content.split()) for m in request.messages) * 1.3
            output_tokens = len(full_response.split()) * 1.3
            
            RateLimiter.increment_monthly_usage(
                current_org.id,
                messages=1,
                tokens=int(input_tokens + output_tokens)
            )
            
            await crud_ai_usage.log_request(
                db, current_org.id, current_user.id, request.model,
                int(input_tokens), int(output_tokens), duration_ms,
                status="success"
            )
        
        except Exception as e:
            logger.error(f"Streaming failed: {e}")
            yield f"data: [ERROR] {str(e)}\n\n"
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )


@router.get("/usage", response_model=UsageSummary)
async def get_usage_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    current_org: Organization = Depends(get_current_organization)
):
    """Get AI usage statistics for current month"""
    # Get subscription for limits
    subscription = await crud_subscription.get_subscription_by_org(db, current_org.id)
    plan_type = subscription.plan_type if subscription else None
    
    messages_limit = get_ai_limit(plan_type, "messages_per_month")
    tokens_limit = get_ai_limit(plan_type, "tokens_per_month")
    
    # Get usage from Redis (fast)
    current_messages = RateLimiter.get_monthly_usage(current_org.id, "messages")
    current_tokens = RateLimiter.get_monthly_usage(current_org.id, "tokens")
    
    # Get detailed breakdown from database
    summary = await crud_ai_usage.get_usage_summary(db, current_org.id)
    
    # Calculate usage percentage
    if messages_limit:
        usage_percentage = (current_messages / messages_limit) * 100
    else:
        usage_percentage = 0  # Unlimited
    
    return UsageSummary(
        total_messages=current_messages,
        total_tokens=current_tokens,
        messages_limit=messages_limit,
        tokens_limit=tokens_limit,
        usage_percentage=round(usage_percentage, 2),
        models_breakdown=summary["models_breakdown"]
    )


@router.get("/models")
async def get_available_models(
    db: AsyncSession = Depends(get_db),
    current_org: Organization = Depends(get_current_organization)
):
    """Get list of available AI models for current plan"""
    subscription = await crud_subscription.get_subscription_by_org(db, current_org.id)
    plan_type = subscription.plan_type if subscription else None
    
    allowed_models = get_ai_limit(plan_type, "allowed_models") or []
    
    from app.core.ai_config import AI_MODELS
    
    models_info = []
    for model_id in allowed_models:
        if model_id in AI_MODELS:
            config = AI_MODELS[model_id]
            models_info.append({
                "id": model_id,
                "name": config["name"],
                "provider": config["provider"],
                "max_tokens": config["max_tokens"]
            })
    
    return {
        "plan": plan_type.value if plan_type else "free",
        "models": models_info
    }
