import redis
from datetime import datetime, timedelta
from typing import Optional
from app.core.config import settings

redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)


class RateLimiter:
    """Redis-based rate limiter"""
    
    @staticmethod
    def check_rate_limit(
        key: str,
        limit: int,
        window_seconds: int = 60
    ) -> tuple[bool, int, int]:
        """
        Check if rate limit is exceeded
        
        Returns: (allowed, current_count, remaining)
        """
        current = redis_client.get(key)
        
        if current is None:
            # First request in window
            redis_client.setex(key, window_seconds, 1)
            return True, 1, limit - 1
        
        current_count = int(current)
        
        if current_count >= limit:
            return False, current_count, 0
        
        # Increment counter
        redis_client.incr(key)
        return True, current_count + 1, limit - current_count - 1
    
    @staticmethod
    def get_monthly_usage(org_id: int, metric: str = "messages") -> int:
        """Get monthly usage from Redis"""
        year_month = datetime.utcnow().strftime("%Y-%m")
        key = f"ai_usage:{org_id}:{year_month}:{metric}"
        
        value = redis_client.get(key)
        return int(value) if value else 0
    
    @staticmethod
    def increment_monthly_usage(
        org_id: int,
        messages: int = 0,
        tokens: int = 0
    ):
        """Increment monthly usage counters"""
        year_month = datetime.utcnow().strftime("%Y-%m")
        
        # Calculate expiry (end of next month)
        now = datetime.utcnow()
        next_month = now.replace(day=28) + timedelta(days=4)
        end_of_next_month = next_month.replace(day=1) + timedelta(days=32)
        end_of_next_month = end_of_next_month.replace(day=1) - timedelta(seconds=1)
        expiry_seconds = int((end_of_next_month - now).total_seconds())
        
        if messages > 0:
            key = f"ai_usage:{org_id}:{year_month}:messages"
            redis_client.incrby(key, messages)
            redis_client.expire(key, expiry_seconds)
        
        if tokens > 0:
            key = f"ai_usage:{org_id}:{year_month}:tokens"
            redis_client.incrby(key, tokens)
            redis_client.expire(key, expiry_seconds)
    
    @staticmethod
    def check_monthly_limit(
        org_id: int,
        messages_limit: Optional[int],
        tokens_limit: Optional[int]
    ) -> tuple[bool, dict]:
        """
        Check if monthly limits are exceeded
        
        Returns: (allowed, usage_info)
        """
        current_messages = RateLimiter.get_monthly_usage(org_id, "messages")
        current_tokens = RateLimiter.get_monthly_usage(org_id, "tokens")
        
        usage_info = {
            "current_messages": current_messages,
            "current_tokens": current_tokens,
            "messages_limit": messages_limit,
            "tokens_limit": tokens_limit
        }
        
        # Check messages limit
        if messages_limit is not None and current_messages >= messages_limit:
            return False, usage_info
        
        # Check tokens limit
        if tokens_limit is not None and current_tokens >= tokens_limit:
            return False, usage_info
        
        return True, usage_info
