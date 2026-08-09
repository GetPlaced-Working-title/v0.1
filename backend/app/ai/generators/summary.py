"""Candidate summary generator."""

from __future__ import annotations

import json
from typing import Any

from app.ai.client import get_gemini_client
from app.ai.prompts.summary import CANDIDATE_SUMMARY_PROMPT
from app.core.logging import get_logger

logger = get_logger(__name__)


class SummaryGenerator:
    """Generates recruiter-facing candidate summaries."""

    def __init__(self) -> None:
        self._client = get_gemini_client()

    async def generate(self, profile: dict[str, Any]) -> dict[str, Any]:
        """Generate a summary for a candidate profile."""
        content = json.dumps(profile, default=str, ensure_ascii=False)[:40000]
        try:
            return await self._client.analyze_text(
                prompt=CANDIDATE_SUMMARY_PROMPT.replace("{profile}", content),
                content="",
            )
        except Exception as e:
            logger.error("summary_generation_failed", error=str(e))
            return self._fallback(profile)

    @staticmethod
    def _fallback(profile: dict[str, Any]) -> dict[str, Any]:
        """Fallback summary when the AI is unavailable."""
        name = profile.get("name") or "Candidate"
        headline = profile.get("headline") or "No headline provided"
        skills = profile.get("skills_graph") or []
        skill_names = ", ".join(s.get("name", "") for s in skills[:10])

        return {
            "quick_read": [
                f"{name} — {headline}",
                f"Skills: {skill_names or 'Not yet analyzed'}",
                f"Evidence confidence: {profile.get('evidence_confidence', 'none')}",
            ],
            "summary": (
                f"{name} is a candidate currently positioned as {headline}. "
                "Full AI analysis is pending — this summary was generated without "
                "AI inference and will be replaced once the profile is analyzed."
            ),
            "proven_evidence": [],
            "claimed_but_unverified": skill_names.split(", ") if skill_names else [],
            "recommended_roles": [],
            "evidence_confidence": profile.get("evidence_confidence", "none"),
            "interview_focus_areas": [],
        }
