"""Project model with AI analysis."""

from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import ARRAY, Boolean, Date, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import SoftDeleteMixin, TimestampMixin


class Project(Base, TimestampMixin, SoftDeleteMixin):
    """Candidate project with AI quality analysis."""

    __tablename__ = "projects"

    candidate_id: Mapped[str] = mapped_column(ForeignKey("candidates.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    role: Mapped[str | None] = mapped_column(String(255), nullable=True)
    technologies: Mapped[list[str] | None] = mapped_column(ARRAY(String), nullable=True)
    url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    github_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    live_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    start_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    is_ongoing: Mapped[bool] = mapped_column(Boolean, default=False)
    scope: Mapped[str | None] = mapped_column(String(50), nullable=True)

    analysis: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    scores: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    source: Mapped[str | None] = mapped_column(String(50), nullable=True)

    processing_status: Mapped[str] = mapped_column(String(50), default="pending")
    processing_error: Mapped[str | None] = mapped_column(Text, nullable=True)
    analyzed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    candidate = relationship("Candidate", back_populates="projects")
