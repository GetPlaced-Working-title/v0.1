"""LinkedIn export model with AI analysis."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import SoftDeleteMixin, TimestampMixin


class LinkedInExport(Base, TimestampMixin, SoftDeleteMixin):
    """LinkedIn profile data (from PDF export or OAuth)."""

    __tablename__ = "linkedin_exports"

    candidate_id: Mapped[str] = mapped_column(ForeignKey("candidates.id"), nullable=False)
    file_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    profile_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    headline: Mapped[str | None] = mapped_column(String(500), nullable=True)
    about: Mapped[str | None] = mapped_column(Text, nullable=True)
    experience: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    education: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    certifications: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    skills: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    recommendations_received: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    endorsements: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    activity: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    analysis: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    scores: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    consistency_flags: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    processing_status: Mapped[str] = mapped_column(String(50), default="pending")
    processing_error: Mapped[str | None] = mapped_column(Text, nullable=True)
    analyzed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    candidate = relationship("Candidate", back_populates="linkedin_export")
