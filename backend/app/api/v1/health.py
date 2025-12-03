from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.database import get_db
from app.core.config import settings
import redis.asyncio as redis
from datetime import datetime

router = APIRouter()


@router.get("/health")
async def health_check():
    """Basic health check"""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/ready")
async def readiness_check(db: AsyncSession = Depends(get_db)):
    """
    Readiness check - verifies all dependencies are available
    Returns 200 if ready, 503 if not ready
    """
    checks = {
        "database": False,
        "redis": False,
        "overall": False
    }
    
    # Check database
    try:
        result = await db.execute(text("SELECT 1"))
        checks["database"] = result.scalar() == 1
    except Exception as e:
        checks["database_error"] = str(e)
    
    # Check Redis
    try:
        redis_client = redis.from_url(settings.REDIS_URL)
        await redis_client.ping()
        checks["redis"] = True
        await redis_client.close()
    except Exception as e:
        checks["redis_error"] = str(e)
    
    # Overall status
    checks["overall"] = checks["database"] and checks["redis"]
    
    status_code = status.HTTP_200_OK if checks["overall"] else status.HTTP_503_SERVICE_UNAVAILABLE
    
    return {
        "status": "ready" if checks["overall"] else "not_ready",
        "checks": checks,
        "timestamp": datetime.utcnow().isoformat()
    }, status_code


@router.get("/live")
async def liveness_check():
    """
    Liveness check - verifies the application is running
    This should always return 200 unless the app is completely dead
    """
    return {
        "status": "alive",
        "timestamp": datetime.utcnow().isoformat()
    }
