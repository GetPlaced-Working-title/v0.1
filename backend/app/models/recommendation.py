"""Recommendation letter model."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import SoftDeleteMixin, TimestampMixin


class Recommendation(Base, TimestampMixin, SoftDeleteMixin):
    """Recommendation letter with AI credibility analysis."""

    __tablename__ = "recommendations"

    candidate_id: Mapped[str] = mapped_column(ForeignKey("candidates.id"), nullable=False)
    recommender_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    recommender_title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    recommender_company: Mapped[str | None] = mapped_column(String(255), nullable=True)
    relation: Mapped[str | None] = mapped_column("relationship", String(100), nullable=True)
    content: Mapped[str | None] = mapped_column(Text, nullable=True)
    file_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    analysis: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    scores: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    source: Mapped[str | None] = mapped_column(String(50), nullable=True)

    processing_status: Mapped[str] = mapped_column(String(50), default="pending")
    processing_error: Mapped[str | None] = mapped_column(Text, nullable=True)
    analyzed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    candidate = relationship("Candidate", back_populates="recommendations")
