"""Matching service — orchestrates vector search + AI reranking."""

from __future__ import annotations

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.matching.embedding import EmbeddingService
from app.ai.matching.hybrid import HybridSearchService
from app.ai.matching.reranker import LLMReranker
from app.core.config import get_settings
from app.core.logging import get_logger
from app.core.qdrant import QdrantService
from app.models.job import Job
from app.models.job_match import JobMatch
from app.repositories.job import JobRepository
from app.repositories.job_match import JobMatchRepository

logger = get_logger(__name__)
settings = get_settings()


class MatchingService:
    """Full matching pipeline: candidate embedding → vector search → rerank → store results."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.match_repo = JobMatchRepository(session)
        self.job_repo = JobRepository(session)
        self.embedding_service = EmbeddingService()
        self.hybrid_search = HybridSearchService()
        self.reranker = LLMReranker()
        self.qdrant = QdrantService()

    async def match_candidates(
        self, job_id: str, top_k: int = 10
    ) -> dict[str, Any]:
        """Run the full matching pipeline for a job."""
        job = await self.job_repo.get_by_id(job_id)
        if not job:
            from app.core.exceptions import NotFoundError
            raise NotFoundError("Job not found")

        # Build job text for embedding
        job_text = self._build_job_text(job)

        # Generate job embedding
        job_embedding = await self.embedding_service.generate_embedding(job_text)

        # Vector search for top candidates
        vector_results = self.qdrant.search(
            collection_name=settings.qdrant_collection_candidates,
            query_vector=job_embedding,
            limit=50,
        )

        if not vector_results:
            return {"job_id": job_id, "matches": [], "total_candidates_evaluated": 0}

        # Rerank top candidates with AI
        candidates_for_rerank = [
            {"candidate_id": r["id"], "vector_score": r["score"], **r.get("payload", {})}
            for r in vector_results
        ]

        reranked = await self.reranker.rerank(
            job_description=job_text,
            candidates=candidates_for_rerank,
            top_k=top_k,
        )

        # Store match results
        matches = []
        for i, match in enumerate(reranked[:top_k]):
            existing = await self.match_repo.get_match(job_id, match["candidate_id"])
            if existing:
                existing.final_score = match.get("final_score", match.get("score", 0))
                existing.vector_score = match.get("vector_score")
                existing.rerank_score = match.get("rerank_score")
                existing.rank = i + 1
                existing.match_details = match.get("details")
                existing.strengths = match.get("strengths")
                existing.gaps = match.get("gaps")
                matches.append(existing)
            else:
                new_match = await self.match_repo.create(
                    job_id=job_id,
                    candidate_id=match["candidate_id"],
                    vector_score=match.get("vector_score"),
                    rerank_score=match.get("rerank_score"),
                    final_score=match.get("final_score", match.get("score", 0)),
                    rank=i + 1,
                    match_details=match.get("details"),
                    strengths=match.get("strengths"),
                    gaps=match.get("gaps"),
                )
                matches.append(new_match)

        # Update job match count
        job.matches_count = len(matches)

        return {
            "job_id": job_id,
            "matches": matches,
            "total_candidates_evaluated": len(vector_results),
        }

    async def get_job_matches(
        self, job_id: str, offset: int = 0, limit: int = 20
    ) -> tuple[list[JobMatch], int]:
        return await self.match_repo.get_by_job(job_id, offset=offset, limit=limit)

    async def update_match_status(self, match_id: str, status: str, notes: str | None = None) -> JobMatch:
        match = await self.match_repo.get_by_id(match_id)
        if not match:
            from app.core.exceptions import NotFoundError
            raise NotFoundError("Match not found")
        match.status = status
        if notes is not None:
            match.recruiter_notes = notes
        return match

    def _build_job_text(self, job: Job) -> str:
        parts = [f"Job Title: {job.title}"]
        parts.append(f"Description: {job.description}")
        if job.required_skills:
            parts.append(f"Required Skills: {', '.join(job.required_skills)}")
        if job.preferred_skills:
            parts.append(f"Preferred Skills: {', '.join(job.preferred_skills)}")
        if job.experience_min is not None:
            parts.append(f"Min Experience: {job.experience_min} years")
        if job.location:
            parts.append(f"Location: {job.location}")
        if job.employment_type:
            parts.append(f"Employment Type: {job.employment_type}")
        return "\n".join(parts)
