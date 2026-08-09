"""LLM reranker — final ranking of top candidates for a job."""

from __future__ import annotations

import json
from typing import Any

from app.ai.client import get_gemini_client
from app.ai.prompts.reranker import RERANKER_PROMPT
from app.core.logging import get_logger

logger = get_logger(__name__)


class LLMReranker:
    """Reranks top candidates using an LLM — evidence-weighted, not keyword-overlap."""

    def __init__(self) -> None:
        self._client = get_gemini_client()

    async def rerank(
        self,
        job: dict[str, Any],
        candidates: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """Rerank candidate matches for a given job."""
        if not candidates:
            return []

        prompt = self._build_prompt(job, candidates)
        try:
            result = await self._client.analyze_text(
                prompt=prompt,
                content="",
            )
            rankings = result.get("rankings", [])
            job_insights = result.get("job_insights", {})
            logger.info("rerank_complete", count=len(rankings))
            return self._attach_rankings(rankings, job_insights)
        except Exception as e:
            # Fail closed: keep hybrid order if the LLM reranker fails
            logger.error("rerank_failed", error=str(e))
            return self._fallback(candidates)

    def _build_prompt(
        self,
        job: dict[str, Any],
        candidates: list[dict[str, Any]],
    ) -> str:
        """Build the reranker prompt with a trimmed candidate view."""
        candidates_json = json.dumps(candidates, default=str, ensure_ascii=False)[:50000]
        return RERANKER_PROMPT.replace("{job_title}", job.get("title", "Unknown Job"))\
            .replace("{job_description}", (job.get("description") or "")[:8000])\
            .replace("{required_skills}", ", ".join(job.get("required_skills", []) or []))\
            .replace("{preferred_skills}", ", ".join(job.get("preferred_skills", []) or []))\
            .replace("{experience_required}", str(job.get("experience_min")))\
            .replace("{candidates}", candidates_json)

    def _attach_rankings(
        self,
        rankings: list[dict[str, Any]],
        job_insights: dict[str, Any],
    ) -> list[dict[str, Any]]:
        """Attach job insights to each ranking."""
        for rank in rankings:
            rank["job_insights"] = job_insights
            rank["rank"] = rank.get("rank", len(rankings))
        rankings.sort(key=lambda r: r.get("rank", 999))
        return rankings

    @staticmethod
    def _fallback(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Fallback ordering when the LLM reranker fails — keep hybrid order."""
        return [
            {
                **c,
                "rank": idx + 1,
                "rerank_score": c.get("hybrid_score", 0),
                "job_insights": {},
            }
            for idx, c in enumerate(candidates)
        ]