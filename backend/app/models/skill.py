"""Skill model with evidence tracking."""

from __future__ import annotations

from datetime import date
from decimal import Decimal

from sqlalchemy import Boolean, Date, ForeignKey, Numeric, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin


class Skill(Base, TimestampMixin):
    """Candidate skill with confidence level based on evidence sources."""

    __tablename__ = "skills"
    __table_args__ = (
        UniqueConstraint("candidate_id", "name", name="uq_skills_candidate_name"),
    )

    candidate_id: Mapped[str] = mapped_column(ForeignKey("candidates.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[str | None] = mapped_column(String(100), nullable=True)
    confidence: Mapped[str] = mapped_column(String(50), default="resume_mention")
    evidence_sources: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    years_of_experience: Mapped[Decimal | None] = mapped_column(Numeric(4, 1), nullable=True)
    last_used_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    proficiency_level: Mapped[str | None] = mapped_column(String(50), nullable=True)
    verified: Mapped[bool] = mapped_column(Boolean, default=False)

    candidate = relationship("Candidate", back_populates="skills")
