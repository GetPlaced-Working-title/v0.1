"""Portfolio model with AI analysis."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import SoftDeleteMixin, TimestampMixin


class Portfolio(Base, TimestampMixin, SoftDeleteMixin):
    """Portfolio website with analyzed projects and design quality."""

    __tablename__ = "portfolios"

    candidate_id: Mapped[str] = mapped_column(ForeignKey("candidates.id"), nullable=False)
    url: Mapped[str] = mapped_column(String(500), nullable=False)
    title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    portfolio_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    projects_found: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    analysis: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    scores: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    screenshots: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    processing_status: Mapped[str] = mapped_column(String(50), default="pending")
    processing_error: Mapped[str | None] = mapped_column(Text, nullable=True)
    last_crawled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    analyzed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    candidate = relationship("Candidate", back_populates="portfolios")
