"""Authentication and authorization using Clerk."""

from __future__ import annotations

from typing import Any

import httpx
from fastapi import Depends, HTTPException, Request, status
from jose import JWTError, jwt

from app.core.config import get_settings

settings = get_settings()

# Cache JWKS keys
_jwks_cache: dict[str, Any] | None = None


async def _get_jwks() -> dict[str, Any]:
    """Fetch and cache JWKS from Clerk."""
    global _jwks_cache
    if _jwks_cache is None:
        async with httpx.AsyncClient() as client:
            response = await client.get(settings.clerk_jwks_url)
            response.raise_for_status()
            _jwks_cache = response.json()
    return _jwks_cache


async def verify_clerk_token(token: str) -> dict[str, Any]:
    """Verify a Clerk JWT and return the payload."""
    jwks = await _get_jwks()

    try:
        # Get the signing key
        unverified_header = jwt.get_unverified_header(token)
        kid = unverified_header.get("kid")

        rsa_key: dict[str, str] = {}
        for key in jwks.get("keys", []):
            if key.get("kid") == kid:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"],
                }
                break

        if not rsa_key:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unable to find signing key",
            )

        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=["RS256"],
            issuer=settings.clerk_issuer,
            options={"verify_aud": False},
        )
        return payload

    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {e!s}",
        )


async def get_current_user(request: Request) -> dict[str, Any]:
    """Extract and verify the current user from the Authorization header."""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid authorization header",
        )

    token = auth_header.split(" ", 1)[1]
    payload = await verify_clerk_token(token)

    return {
        "clerk_id": payload.get("sub"),
        "email": payload.get("email"),
        "role": payload.get("metadata", {}).get("role", "candidate"),
    }


def role_required(*roles: str):
    """Dependency factory that checks user role."""

    async def check_role(
        current_user: dict[str, Any] = Depends(get_current_user),
    ) -> dict[str, Any]:
        if current_user.get("role") not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        return current_user

    return check_role
