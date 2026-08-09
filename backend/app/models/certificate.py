"""Certificate model with AI analysis."""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import ARRAY, Boolean, Date, DateTime, ForeignKey, Numeric, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import SoftDeleteMixin, TimestampMixin


class Certificate(Base, TimestampMixin, SoftDeleteMixin):
    """Certification with verification and AI credibility analysis."""

    __tablename__ = "certificates"

    candidate_id: Mapped[str] = mapped_column(ForeignKey("candidates.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    issuer: Mapped[str | None] = mapped_column(String(255), nullable=True)
    issue_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    expiry_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    credential_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    credential_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    file_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    difficulty_level: Mapped[str | None] = mapped_column(String(50), nullable=True)
    assessment_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    learning_hours: Mapped[Decimal | None] = mapped_column(Numeric(6, 1), nullable=True)
    skills_covered: Mapped[list[str] | None] = mapped_column(ARRAY(String), nullable=True)

    analysis: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    scores: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    verification_method: Mapped[str | None] = mapped_column(String(50), nullable=True)
    source: Mapped[str | None] = mapped_column(String(50), nullable=True)

    processing_status: Mapped[str] = mapped_column(String(50), default="pending")
    processing_error: Mapped[str | None] = mapped_column(Text, nullable=True)
    analyzed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    candidate = relationship("Candidate", back_populates="certificates")
