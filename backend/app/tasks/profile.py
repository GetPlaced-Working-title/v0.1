"""Celery tasks for profile building."""

from __future__ import annotations

from app.core.celery_app import celery_app
from app.core.logging import get_logger

logger = get_logger(__name__)


@celery_app.task(name="app.tasks.profile.build_profile")
def build_profile(candidate_id: str) -> dict:
    """Aggregate all analyses into a unified candidate profile."""
    import asyncio
    return asyncio.run(_build_profile_async(candidate_id))


async def _build_profile_async(candidate_id: str) -> dict:
    from app.core.database import async_session_factory
    from app.ai.scoring.profile_builder import ProfileBuilder
    from app.repositories.candidate import CandidateRepository
    from app.repositories.resume import ResumeRepository
    from app.repositories.github import GitHubProfileRepository
    from app.repositories.portfolio import PortfolioRepository
    from app.repositories.skill import SkillRepository

    async with async_session_factory() as session:
        candidate_repo = CandidateRepository(session)
        candidate = await candidate_repo.get_by_id(candidate_id)
        if not candidate:
            return {"error": "Candidate not found"}

        try:
            builder = ProfileBuilder()

            # Collect resume analysis
            resume_repo = ResumeRepository(session)
            resumes = await resume_repo.get_by_candidate(candidate_id)
            for resume in resumes:
                if resume.analysis:
                    builder.add_analysis("resume", resume.analysis)

            # Collect GitHub analysis
            github_repo = GitHubProfileRepository(session)
            github = await github_repo.get_by_candidate(candidate_id)
            if github and github.analysis:
                builder.add_analysis("github", github.analysis)

            # Collect portfolio analysis
            portfolio_repo = PortfolioRepository(session)
            portfolios = await portfolio_repo.get_by_candidate(candidate_id)
            for portfolio in portfolios:
                if portfolio.analysis:
                    builder.add_analysis("portfolio", portfolio.analysis)

            # Build the profile
            profile = builder.build()

            # Update candidate
            candidate.overall_scores = profile.get("aggregate_scores", {})
            candidate.evidence_confidence = profile.get("evidence_confidence", "none")

            # Update skills
            skill_repo = SkillRepository(session)
            skills = profile.get("skills_graph", [])
            for skill_data in skills:
                await skill_repo.upsert_skill(
                    candidate_id=candidate_id,
                    name=skill_data["name"],
                    category=skill_data.get("category"),
                    confidence=skill_data.get("confidence", "resume_mention"),
                    evidence_sources=skill_data.get("evidence_sources"),
                    verified=skill_data.get("verified", False),
                )

            from datetime import datetime, timezone
            candidate.last_analyzed_at = datetime.now(timezone.utc)
            await session.commit()

            # Generate embedding
            from app.tasks.embedding import generate_candidate_embedding
            generate_candidate_embedding.delay(candidate_id)

            return {"status": "completed", "candidate_id": candidate_id}

        except Exception as e:
            logger.error("profile_build_failed", candidate_id=candidate_id, error=str(e))
            return {"status": "failed", "error": str(e)}
