"""Global error handling middleware."""

from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.exceptions import AppException
from app.core.logging import get_logger

logger = get_logger(__name__)


def setup_error_handlers(app: FastAPI) -> None:
    """Register global error handlers."""

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
        request_id = getattr(request.state, "request_id", "unknown")
        logger.warning(
            "app_error",
            status_code=exc.status_code,
            detail=exc.detail,
            request_id=request_id,
            path=str(request.url),
        )
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.detail,
                "request_id": request_id,
            },
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        request_id = getattr(request.state, "request_id", "unknown")
        logger.error(
            "unhandled_error",
            error=str(exc),
            error_type=type(exc).__name__,
            request_id=request_id,
            path=str(request.url),
            exc_info=True,
        )

        from app.core.config import get_settings
        settings = get_settings()

        detail = str(exc) if settings.debug else "Internal server error"
        return JSONResponse(
            status_code=500,
            content={
                "error": detail,
                "request_id": request_id,
            },
        )
