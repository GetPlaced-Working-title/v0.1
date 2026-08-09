"""Custom application exceptions."""

from __future__ import annotations


class AppException(Exception):
    """Base application exception."""

    status_code: int = 500
    detail: str = "Internal server error"

    def __init__(self, detail: str | None = None, status_code: int | None = None) -> None:
        self.detail = detail or self.__class__.detail
        if status_code is not None:
            self.status_code = status_code
        super().__init__(self.detail)


class NotFoundError(AppException):
    status_code = 404
    detail = "Resource not found"


class ConflictError(AppException):
    status_code = 409
    detail = "Resource already exists"


class ValidationError(AppException):
    status_code = 422
    detail = "Validation error"


class UnauthorizedError(AppException):
    status_code = 401
    detail = "Not authenticated"


class ForbiddenError(AppException):
    status_code = 403
    detail = "Insufficient permissions"


class AIAnalysisError(AppException):
    status_code = 502
    detail = "AI analysis failed"


class StorageError(AppException):
    status_code = 502
    detail = "Storage operation failed"


class ExternalServiceError(AppException):
    status_code = 502
    detail = "External service unavailable"


class RateLimitError(AppException):
    status_code = 429
    detail = "Too many requests"
