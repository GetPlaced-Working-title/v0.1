"""Application configuration using Pydantic Settings."""

from functools import lru_cache
from typing import Any

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # App
    app_name: str = "AI Talent Router"
    app_env: str = "development"
    debug: bool = False
    api_version: str = "v1"
    cors_origins: list[str] = ["http://localhost:3000"]

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: Any) -> list[str]:
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    # Database
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/talent_ai"
    database_pool_size: int = 20
    database_max_overflow: int = 10

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # Qdrant
    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: str = ""
    qdrant_collection_candidates: str = "candidates"
    qdrant_collection_jobs: str = "jobs"
    qdrant_vector_size: int = 768

    # Meilisearch
    meilisearch_url: str = "http://localhost:7700"
    meilisearch_api_key: str = "masterKey"

    # Cloudflare R2
    r2_endpoint_url: str = ""
    r2_access_key_id: str = ""
    r2_secret_access_key: str = ""
    r2_bucket_name: str = "talent-ai"
    r2_public_url: str = ""

    # Gemini AI
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.0-flash-lite"
    gemini_video_model: str = "gemini-2.0-flash"
    gemini_embedding_model: str = "text-embedding-004"

    # Clerk Auth
    clerk_secret_key: str = ""
    clerk_jwks_url: str = ""
    clerk_issuer: str = ""

    # Celery
    celery_broker_url: str = "redis://localhost:6379/1"
    celery_result_backend: str = "redis://localhost:6379/2"

    # Logging
    log_level: str = "INFO"
    log_format: str = "json"

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"

    @property
    def is_development(self) -> bool:
        return self.app_env == "development"


@lru_cache
def get_settings() -> Settings:
    """Cached settings instance."""
    return Settings()
