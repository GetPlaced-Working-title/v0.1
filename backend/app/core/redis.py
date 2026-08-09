"""Redis client with caching support."""

from __future__ import annotations

import json
from typing import Any

import redis.asyncio as aioredis

from app.core.config import get_settings

settings = get_settings()

_redis_client: aioredis.Redis | None = None


async def get_redis() -> aioredis.Redis:
    """Get or create the Redis client singleton."""
    global _redis_client
    if _redis_client is None:
        _redis_client = aioredis.from_url(
            settings.redis_url,
            decode_responses=True,
            max_connections=20,
        )
    return _redis_client


async def close_redis() -> None:
    """Close the Redis connection."""
    global _redis_client
    if _redis_client is not None:
        await _redis_client.close()
        _redis_client = None


class RedisCache:
    """High-level Redis cache operations."""

    def __init__(self, client: aioredis.Redis) -> None:
        self._client = client

    async def get(self, key: str) -> Any | None:
        """Get a value, deserializing JSON if possible."""
        value = await self._client.get(key)
        if value is None:
            return None
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return value

    async def set(
        self,
        key: str,
        value: Any,
        ttl: int | None = None,
    ) -> None:
        """Set a value, serializing to JSON."""
        serialized = json.dumps(value) if not isinstance(value, str) else value
        if ttl:
            await self._client.setex(key, ttl, serialized)
        else:
            await self._client.set(key, serialized)

    async def delete(self, key: str) -> None:
        """Delete a key."""
        await self._client.delete(key)

    async def get_or_set(
        self,
        key: str,
        factory: Any,
        ttl: int = 3600,
    ) -> Any:
        """Get value from cache or compute and store it."""
        cached = await self.get(key)
        if cached is not None:
            return cached

        if callable(factory):
            is_awaitable = hasattr(factory, "__await__")
            value = await factory() if is_awaitable or callable(factory) else factory
            if callable(value):
                value = await value()
        else:
            value = factory

        await self.set(key, value, ttl=ttl)
        return value

    async def exists(self, key: str) -> bool:
        """Check if key exists."""
        return bool(await self._client.exists(key))

    async def increment(self, key: str, amount: int = 1) -> int:
        """Increment a counter."""
        return await self._client.incrby(key, amount)

    async def expire(self, key: str, ttl: int) -> None:
        """Set expiration on a key."""
        await self._client.expire(key, ttl)

    async def flush_pattern(self, pattern: str) -> int:
        """Delete all keys matching a pattern."""
        count = 0
        async for key in self._client.scan_iter(match=pattern):
            await self._client.delete(key)
            count += 1
        return count
