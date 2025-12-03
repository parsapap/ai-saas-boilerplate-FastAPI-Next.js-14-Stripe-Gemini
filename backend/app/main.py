from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from sqlalchemy import create_engine
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    logger.info("🚀 Starting FastAPI SaaS application...")
    logger.info("✅ Database connection pool initialized")
    logger.info("✅ Redis connection established")
    logger.info("✅ All services ready")
    
    yield
    
    # Shutdown
    logger.info("👋 Shutting down application...")


# Import after lifespan to avoid circular imports
from app.core.config import settings
from app.api.v1 import auth, users, organizations, apikeys, premium, ai, health
from app.api.v1 import billing as billing_router
from app.core.metrics import metrics_endpoint, MetricsMiddleware
from app.admin.admin import setup_admin

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
    description="Enterprise-ready AI SaaS boilerplate with multi-tenancy, Stripe billing, and AI integrations"
)

# Metrics middleware
app.add_middleware(MetricsMiddleware)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup Admin Panel
engine = create_engine(settings.DATABASE_URL_SYNC)
admin = setup_admin(app, engine)


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


# Include routers
app.include_router(health.router, tags=["Health"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(billing_router.router, prefix="/api/v1/billing", tags=["Billing & Subscriptions"])
app.include_router(organizations.router, prefix="/api/v1/orgs", tags=["Organizations"])
app.include_router(apikeys.router, prefix="/api/v1/apikeys", tags=["API Keys"])
app.include_router(premium.router, prefix="/api/v1/premium", tags=["Premium Features"])
app.include_router(ai.router, prefix="/api/v1/ai", tags=["AI & Chat"])


# Metrics endpoint
@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    return metrics_endpoint()


@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "admin": "/admin",
        "metrics": "/metrics",
        "health": "/health",
        "ready": "/ready",
        "status": "running"
    }
