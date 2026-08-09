"""Celery tasks for portfolio analysis."""

from __future__ import annotations

from datetime import UTC

from app.core.celery_app import celery_app
from app.core.logging import get_logger

logger = get_logger(__name__)


@celery_app.task(name="app.tasks.portfolio.analyze_portfolio")
def analyze_portfolio(portfolio_id: str) -> dict:
    """Analyze a portfolio website."""
    import asyncio
    return asyncio.run(_analyze_portfolio_async(portfolio_id))


async def _analyze_portfolio_async(portfolio_id: str) -> dict:
    from app.ai.analyzers.portfolio import PortfolioAnalyzer
    from app.core.database import async_session_factory
    from app.models.portfolio import Portfolio
    from app.repositories.base import BaseRepository

    async with async_session_factory() as session:
        repo = BaseRepository(Portfolio, session)
        portfolio = await repo.get_by_id(portfolio_id)
        if not portfolio:
            return {"error": "Portfolio not found"}

        try:
            portfolio.processing_status = "processing"
            await session.commit()

            analyzer = PortfolioAnalyzer()
            analysis = await analyzer.analyze(portfolio.url, session)

            portfolio.analysis = analysis
            portfolio.scores = analysis.get("scores", {})

            from datetime import datetime
            portfolio.analyzed_at = datetime.now(UTC)
            portfolio.last_crawled_at = datetime.now(UTC)
            portfolio.processing_status = "completed"
            await session.commit()

            return {"status": "completed", "portfolio_id": portfolio_id}

        except Exception as e:
            portfolio.processing_status = "failed"
            portfolio.processing_error = str(e)
            await session.commit()
            return {"status": "failed", "error": str(e)}
