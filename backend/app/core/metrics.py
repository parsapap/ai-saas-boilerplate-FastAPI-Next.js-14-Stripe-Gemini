from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Response
import time

# Request metrics
http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint']
)

# Business metrics
user_registrations_total = Counter(
    'user_registrations_total',
    'Total user registrations'
)

subscriptions_total = Counter(
    'subscriptions_total',
    'Total subscriptions',
    ['plan_type']
)

subscriptions_active = Gauge(
    'subscriptions_active',
    'Currently active subscriptions',
    ['plan_type']
)

ai_requests_total = Counter(
    'ai_requests_total',
    'Total AI requests',
    ['provider', 'model']
)

ai_tokens_used_total = Counter(
    'ai_tokens_used_total',
    'Total AI tokens used',
    ['provider', 'model']
)

api_key_requests_total = Counter(
    'api_key_requests_total',
    'Total API key requests',
    ['organization_id']
)

stripe_webhooks_total = Counter(
    'stripe_webhooks_total',
    'Total Stripe webhooks received',
    ['event_type', 'status']
)

# Database metrics
db_connections_active = Gauge(
    'db_connections_active',
    'Active database connections'
)

redis_connections_active = Gauge(
    'redis_connections_active',
    'Active Redis connections'
)


def metrics_endpoint():
    """Prometheus metrics endpoint"""
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )


class MetricsMiddleware:
    """Middleware to track request metrics"""
    
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        
        method = scope["method"]
        path = scope["path"]
        
        # Skip metrics endpoint itself
        if path == "/metrics":
            await self.app(scope, receive, send)
            return
        
        start_time = time.time()
        
        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                status_code = message["status"]
                duration = time.time() - start_time
                
                # Record metrics
                http_requests_total.labels(
                    method=method,
                    endpoint=path,
                    status=status_code
                ).inc()
                
                http_request_duration_seconds.labels(
                    method=method,
                    endpoint=path
                ).observe(duration)
            
            await send(message)
        
        await self.app(scope, receive, send_wrapper)
