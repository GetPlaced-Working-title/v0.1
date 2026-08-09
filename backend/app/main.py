"""FastAPI application entry point."""

from __future__ import annotations

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import get_settings
from app.core.database import close_db, init_db
from app.core.logging import get_logger, setup_logging
from app.core.redis import close_redis

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application startup and shutdown."""
    setup_logging()
    settings = get_settings()

    logger.info("starting", app=settings.app_name, env=settings.app_env)

    # Initialize database
    await init_db()
    logger.info("database_ready")

    # Initialize Qdrant collections
    try:
        from app.core.qdrant import QdrantService
        qdrant = QdrantService()
        qdrant.ensure_collection(settings.qdrant_collection_candidates)
        qdrant.ensure_collection(settings.qdrant_collection_jobs)
        logger.info("qdrant_ready")
    except Exception as e:
        logger.warning("qdrant_init_failed", error=str(e))

    # Initialize Meilisearch indexes
    try:
        from app.core.meilisearch import MeilisearchService
        meili = MeilisearchService()
        meili.ensure_index(
            "candidates",
            searchable_attributes=[
                "name", "headline", "skills", "location",
                "current_role", "current_company",
            ],
            filterable_attributes=[
                "location", "years_of_experience", "evidence_confidence",
                "availability", "open_to_remote",
            ],
            sortable_attributes=["years_of_experience", "created_at"],
        )
        meili.ensure_index(
            "jobs",
            searchable_attributes=[
                "title", "description", "required_skills",
                "preferred_skills", "location",
            ],
            filterable_attributes=[
                "status", "employment_type", "work_mode", "location",
            ],
            sortable_attributes=["created_at"],
        )
        logger.info("meilisearch_ready")
    except Exception as e:
        logger.warning("meilisearch_init_failed", error=str(e))

    yield

    # Shutdown
    await close_db()
    await close_redis()
    from app.core.qdrant import close_qdrant
    close_qdrant()
    logger.info("shutdown_complete")


def create_app() -> FastAPI:
    """Application factory."""
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        description="AI-powered hiring platform that understands candidates from evidence.",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    # Middleware
    from app.middleware.cors import setup_cors
    from app.middleware.error_handler import setup_error_handlers
    from app.middleware.request_id import RequestIDMiddleware

    setup_cors(app)
    app.add_middleware(RequestIDMiddleware)
    setup_error_handlers(app)

    # Routers
    from app.routers.admin import router as admin_router
    from app.routers.auth import router as auth_router
    from app.routers.candidates import router as candidates_router
    from app.routers.certificates import router as certificates_router
    from app.routers.companies import router as companies_router
    from app.routers.github import router as github_router
    from app.routers.health import router as health_router
    from app.routers.jobs import router as jobs_router
    from app.routers.matching import router as matching_router
    from app.routers.portfolios import router as portfolios_router
    from app.routers.resumes import router as resumes_router
    from app.routers.search import router as search_router
    from app.routers.videos import router as videos_router

    prefix = f"/api/{settings.api_version}"

    app.include_router(health_router)
    app.include_router(auth_router, prefix=f"{prefix}/auth")
    app.include_router(candidates_router, prefix=f"{prefix}/candidates")
    app.include_router(companies_router, prefix=f"{prefix}/companies")
    app.include_router(jobs_router, prefix=f"{prefix}/jobs")
    app.include_router(resumes_router, prefix=f"{prefix}/resumes")
    app.include_router(github_router, prefix=f"{prefix}/github")
    app.include_router(portfolios_router, prefix=f"{prefix}/portfolios")
    app.include_router(videos_router, prefix=f"{prefix}/videos")
    app.include_router(certificates_router, prefix=f"{prefix}/certificates")
    app.include_router(search_router, prefix=f"{prefix}/search")
    app.include_router(matching_router, prefix=f"{prefix}/matching")
    app.include_router(admin_router, prefix=f"{prefix}/admin")

    return app


app = create_app()
