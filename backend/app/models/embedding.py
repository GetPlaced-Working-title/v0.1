"""Embedding record model."""

from __future__ import annotations

from sqlalchemy import Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.base import TimestampMixin


class Embedding(Base, TimestampMixin):
    """Track embedding vectors stored in Qdrant."""

    __tablename__ = "embeddings"

    entity_type: Mapped[str] = mapped_column(String(50), nullable=False)  # candidate, job
    entity_id: Mapped[str] = mapped_column(String(255), nullable=False)
    qdrant_point_id: Mapped[str] = mapped_column(String(255), nullable=False)
    collection_name: Mapped[str] = mapped_column(String(100), nullable=False)
    model_used: Mapped[str | None] = mapped_column(String(100), nullable=True)
    vector_dimension: Mapped[int | None] = mapped_column(Integer, nullable=True)
    input_text_hash: Mapped[str | None] = mapped_column(String(64), nullable=True)
    extra: Mapped[dict | None] = mapped_column("metadata", JSONB, nullable=True)
