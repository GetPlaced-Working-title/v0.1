"""Health check router."""

from __future__ import annotations

from fastapi import APIRouter

from app.core.config import get_settings
from app.core.logging import get_logger

router = APIRouter(tags=["health"])
logger = get_logger(__name__)


@router.get("/health")
async def health_check() -> dict[str, str]:
    """Basic health check."""
    return {"status": "healthy"}


@router.get("/health/ready")
async def readiness_check() -> dict[str, object]:
    """Check all service connections."""
    settings = get_settings()
    checks: dict[str, object] = {}

    # Check database
    try:
        from app.core.database import engine
        async with engine.connect() as conn:
            await conn.execute(
                __import__("sqlalchemy").text("SELECT 1")
            )
        checks["database"] = "ok"
    except Exception as e:
        checks["database"] = f"error: {e!s}"

    # Check Redis
    try:
        from app.core.redis import get_redis
        redis = await get_redis()
        await redis.ping()
        checks["redis"] = "ok"
    except Exception as e:
        checks["redis"] = f"error: {e!s}"

    # Check Qdrant
    try:
        from app.core.qdrant import get_qdrant
        client = get_qdrant()
        client.get_collections()
        checks["qdrant"] = "ok"
    except Exception as e:
        checks["qdrant"] = f"error: {e!s}"

    # Check Meilisearch
    try:
        from app.core.meilisearch import get_meilisearch
        client = get_meilisearch()
        client.health()
        checks["meilisearch"] = "ok"
    except Exception as e:
        checks["meilisearch"] = f"error: {e!s}"

    all_ok = all(v == "ok" for v in checks.values())
    return {
        "status": "ready" if all_ok else "degraded",
        "checks": checks,
    }
