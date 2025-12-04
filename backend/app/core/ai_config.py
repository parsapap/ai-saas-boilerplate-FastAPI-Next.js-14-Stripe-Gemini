from app.models.subscription import PlanType
from decimal import Decimal

# AI Model configurations
AI_MODELS = {
    "gemini-2.0-flash": {
        "provider": "google",
        "name": "Gemini 2.0 Flash",
        "max_tokens": 8192,
        "cost_per_1k_input": Decimal("0.00035"),  # Same as 1.5 Flash
        "cost_per_1k_output": Decimal("0.00105"),
    },
    "gemini-1.5-flash": {
        "provider": "google",
        "name": "Gemini 1.5 Flash",
        "max_tokens": 8192,
        "cost_per_1k_input": Decimal("0.00035"),  # $0.00035 per 1K tokens
        "cost_per_1k_output": Decimal("0.00105"),
    },
    "gemini-1.5-pro": {
        "provider": "google",
        "name": "Gemini 1.5 Pro",
        "max_tokens": 8192,
        "cost_per_1k_input": Decimal("0.00125"),
        "cost_per_1k_output": Decimal("0.00375"),
    },
    "claude-3-haiku": {
        "provider": "anthropic",
        "name": "Claude 3 Haiku",
        "max_tokens": 4096,
        "cost_per_1k_input": Decimal("0.00025"),
        "cost_per_1k_output": Decimal("0.00125"),
    },
    "gpt-4o-mini": {
        "provider": "openai",
        "name": "GPT-4o Mini",
        "max_tokens": 16384,
        "cost_per_1k_input": Decimal("0.00015"),
        "cost_per_1k_output": Decimal("0.00060"),
    }
}

# Plan-based AI limits
AI_LIMITS = {
    PlanType.FREE: {
        "messages_per_month": 50,
        "tokens_per_month": 50000,
        "allowed_models": ["gemini-2.0-flash", "gemini-1.5-flash", "gpt-4o-mini"],
        "max_tokens_per_request": 1024,
        "rate_limit_per_minute": 5,
    },
    PlanType.PRO: {
        "messages_per_month": 10000,
        "tokens_per_month": 10000000,  # 10M tokens
        "allowed_models": ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-pro", "claude-3-haiku", "gpt-4o-mini"],
        "max_tokens_per_request": 4096,
        "rate_limit_per_minute": 60,
    },
    PlanType.TEAM: {
        "messages_per_month": None,  # Unlimited
        "tokens_per_month": None,
        "allowed_models": ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-pro", "claude-3-haiku", "gpt-4o-mini"],
        "max_tokens_per_request": 8192,
        "rate_limit_per_minute": 300,
    }
}


def get_ai_limit(plan_type: PlanType, limit_name: str):
    """Get AI limit for a plan"""
    return AI_LIMITS.get(plan_type, {}).get(limit_name)


def calculate_cost(model: str, input_tokens: int, output_tokens: int) -> int:
    """Calculate cost in cents"""
    if model not in AI_MODELS:
        return 0
    
    config = AI_MODELS[model]
    input_cost = (input_tokens / 1000) * config["cost_per_1k_input"]
    output_cost = (output_tokens / 1000) * config["cost_per_1k_output"]
    
    total_cost_dollars = input_cost + output_cost
    return int(total_cost_dollars * 100)  # Convert to cents
