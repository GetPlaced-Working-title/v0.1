"""AI analysis cache model."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Integer, Numeric, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.base import TimestampMixin


class AIAnalysisCache(Base, TimestampMixin):
    """Cache AI analysis results to avoid duplicate calls."""

    __tablename__ = "ai_analysis_cache"

    input_hash: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    analyzer_type: Mapped[str] = mapped_column(String(100), nullable=False)
    model_used: Mapped[str | None] = mapped_column(String(100), nullable=True)
    input_tokens: Mapped[int | None] = mapped_column(Integer, nullable=True)
    output_tokens: Mapped[int | None] = mapped_column(Integer, nullable=True)
    result: Mapped[dict] = mapped_column(JSONB, nullable=False)
    cost_usd: Mapped[Decimal | None] = mapped_column(Numeric(10, 6), nullable=True)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
