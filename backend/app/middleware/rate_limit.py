"""Rate limiting middleware using Redis."""

from __future__ import annotations

from fastapi import HTTPException, Request, status

from app.core.redis import get_redis


class RateLimiter:
    """Token bucket rate limiter backed by Redis."""

    def __init__(self, requests_per_minute: int = 60) -> None:
        self.requests_per_minute = requests_per_minute

    async def __call__(self, request: Request) -> None:
        """Check rate limit for the current request."""
        client_ip = request.client.host if request.client else "unknown"
        key = f"rate_limit:{client_ip}:{request.url.path}"

        redis = await get_redis()
        current = await redis.incr(key)

        if current == 1:
            await redis.expire(key, 60)

        if current > self.requests_per_minute:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many requests. Please try again later.",
            )


def rate_limit(requests_per_minute: int = 60) -> RateLimiter:
    """Create a rate limiter dependency."""
    return RateLimiter(requests_per_minute=requests_per_minute)
