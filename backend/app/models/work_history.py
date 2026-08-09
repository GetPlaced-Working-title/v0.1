"""Work history model."""

from __future__ import annotations

from datetime import date

from sqlalchemy import ARRAY, Boolean, Date, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import SoftDeleteMixin, TimestampMixin


class WorkHistory(Base, TimestampMixin, SoftDeleteMixin):
    """Individual work experience entry with AI analysis."""

    __tablename__ = "work_history"

    candidate_id: Mapped[str] = mapped_column(ForeignKey("candidates.id"), nullable=False)
    company: Mapped[str] = mapped_column(String(255), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    location: Mapped[str | None] = mapped_column(String(255), nullable=True)
    start_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    is_current: Mapped[bool] = mapped_column(Boolean, default=False)
    employment_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    responsibilities: Mapped[list[str] | None] = mapped_column(ARRAY(String), nullable=True)
    achievements: Mapped[list[str] | None] = mapped_column(ARRAY(String), nullable=True)
    technologies: Mapped[list[str] | None] = mapped_column(ARRAY(String), nullable=True)

    analysis: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    scores: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    source: Mapped[str | None] = mapped_column(String(50), nullable=True)

    candidate = relationship("Candidate", back_populates="work_history")
