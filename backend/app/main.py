from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1 import auth, users, organizations, apikeys
from app.api.v1 import billing as billing_router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(billing_router.router, prefix="/api/v1/billing", tags=["Billing & Subscriptions"])
app.include_router(organizations.router, prefix="/api/v1/orgs", tags=["Organizations"])
app.include_router(apikeys.router, prefix="/api/v1/apikeys", tags=["API Keys"])

# Premium features (example)
from app.api.v1 import premium
app.include_router(premium.router, prefix="/api/v1/premium", tags=["Premium Features"])

# AI endpoints
from app.api.v1 import ai
app.include_router(ai.router, prefix="/api/v1/ai", tags=["AI & Chat"])


@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
