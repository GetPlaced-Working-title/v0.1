"""Celery tasks for embedding generation."""

from __future__ import annotations

from app.core.celery_app import celery_app
from app.core.config import get_settings
from app.core.logging import get_logger

logger = get_logger(__name__)
settings = get_settings()


@celery_app.task(name="app.tasks.embedding.generate_candidate_embedding")
def generate_candidate_embedding(candidate_id: str) -> dict:
    """Generate and store a candidate's profile embedding in Qdrant."""
    import asyncio
    return asyncio.run(_generate_candidate_embedding_async(candidate_id))


async def _generate_candidate_embedding_async(candidate_id: str) -> dict:
    from app.core.database import async_session_factory
    from app.core.qdrant import QdrantService
    from app.ai.client import get_gemini_client
    from app.repositories.candidate import CandidateRepository

    async with async_session_factory() as session:
        repo = CandidateRepository(session)
        candidate = await repo.get_by_id(candidate_id)
        if not candidate:
            return {"error": "Candidate not found"}

        try:
            client = get_gemini_client()
            qdrant = QdrantService()

            # Build text for embedding
            parts = [candidate.name or ""]
            if candidate.headline:
                parts.append(candidate.headline)
            if candidate.bio:
                parts.append(candidate.bio)
            if candidate.current_role:
                parts.append(f"Current role: {candidate.current_role}")
            if candidate.overall_scores:
                import json
                parts.append(f"Scores: {json.dumps(candidate.overall_scores)}")

            text = " ".join(parts)
            vector = await client.generate_embedding(text)

            qdrant.upsert_vector(
                collection_name=settings.qdrant_collection_candidates,
                point_id=candidate_id,
                vector=vector,
                payload={
                    "name": candidate.name,
                    "headline": candidate.headline,
                    "location": candidate.location,
                    "years_of_experience": float(candidate.years_of_experience) if candidate.years_of_experience else 0,
                },
            )

            candidate.profile_embedding_id = candidate_id
            await session.commit()

            return {"status": "completed", "candidate_id": candidate_id}

        except Exception as e:
            logger.error("embedding_failed", candidate_id=candidate_id, error=str(e))
            return {"status": "failed", "error": str(e)}


@celery_app.task(name="app.tasks.embedding.generate_job_embedding")
def generate_job_embedding(job_id: str) -> dict:
    """Generate and store a job's embedding in Qdrant."""
    import asyncio
    return asyncio.run(_generate_job_embedding_async(job_id))


async def _generate_job_embedding_async(job_id: str) -> dict:
    from app.core.database import async_session_factory
    from app.core.qdrant import QdrantService
    from app.ai.client import get_gemini_client
    from app.repositories.job import JobRepository

    async with async_session_factory() as session:
        repo = JobRepository(session)
        job = await repo.get_by_id(job_id)
        if not job:
            return {"error": "Job not found"}

        try:
            client = get_gemini_client()
            qdrant = QdrantService()

            parts = [job.title, job.description]
            if job.required_skills:
                parts.append(f"Required skills: {', '.join(job.required_skills)}")
            if job.preferred_skills:
                parts.append(f"Preferred skills: {', '.join(job.preferred_skills)}")

            text = " ".join(parts)
            vector = await client.generate_embedding(text)

            qdrant.upsert_vector(
                collection_name=settings.qdrant_collection_jobs,
                point_id=job_id,
                vector=vector,
                payload={
                    "title": job.title,
                    "company_id": job.company_id,
                    "location": job.location,
                    "employment_type": job.employment_type,
                },
            )

            job.embedding_id = job_id
            await session.commit()

            return {"status": "completed", "job_id": job_id}

        except Exception as e:
            logger.error("job_embedding_failed", job_id=job_id, error=str(e))
            return {"status": "failed", "error": str(e)}
