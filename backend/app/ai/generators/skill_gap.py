"""Skill gap analyzer and learning roadmap generators."""

from __future__ import annotations

import json
from typing import Any

from app.ai.client import get_gemini_client
from app.ai.prompts.skill_gap import LEARNING_ROADMAP_PROMPT, SKILL_GAP_ANALYSIS_PROMPT
from app.core.logging import get_logger

logger = get_logger(__name__)


class SkillGapAnalyzer:
    """Compares candidate skills against job requirements."""

    def __init__(self) -> None:
        self._client = get_gemini_client()

    async def analyze(
        self,
        job_requirements: dict[str, Any],
        candidate_skills: list[str],
    ) -> dict[str, Any]:
        """Determine skill gaps between a candidate and a target job."""
        prompt = SKILL_GAP_ANALYSIS_PROMPT.replace(
            "{job_requirements}", json.dumps(job_requirements, default=str)
        ).replace("{candidate_skills}", json.dumps(candidate_skills, default=str))

        try:
            return await self._client.analyze_text(prompt=prompt, content="")
        except Exception as e:
            logger.error("skill_gap_failed", error=str(e))
            return self._fallback(job_requirements, candidate_skills)

    @staticmethod
    def _fallback(
        job_requirements: dict[str, Any],
        candidate_skills: list[str],
    ) -> dict[str, Any]:
        """Deterministic fallback: flag required skills not in candidate set."""
        required = set(job_requirements.get("required_skills") or [])
        candidate = {s.lower() for s in candidate_skills}
        missing = sorted(r for r in required if r.lower() not in candidate)
        coverage = (len(required) - len(missing)) / max(1, len(required))
        return {
            "skill_gaps": [
                {
                    "skill": skill,
                    "status": "missing",
                    "gap_severity": "major",
                    "importance": "required",
                    "mitigation": "None — not found in verified skills",
                    "suggested_evidence": "Add project, GitHub, or assessment evidence",
                }
                for skill in missing
            ],
            "overall_gap_score": round(coverage * 100, 1),
            "summary": f"Missing {len(missing)} of {len(required)} required skills.",
        }


class LearningRoadmapGenerator:
    """Builds a personalized learning roadmap to close skill gaps."""

    def __init__(self) -> None:
        self._client = get_gemini_client()

    async def generate(
        self,
        target_role: str,
        skills_to_acquire: list[str],
        candidate_background: str,
    ) -> dict[str, Any]:
        """Generate a learning roadmap."""
        prompt = LEARNING_ROADMAP_PROMPT
        prompt = prompt.replace("{target_role}", target_role)
        prompt = prompt.replace("{skills_to_acquire}", json.dumps(skills_to_acquire))
        prompt = prompt.replace("{candidate_background}", candidate_background or "Unknown")

        try:
            return await self._client.analyze_text(prompt=prompt, content="")
        except Exception as e:
            logger.error("roadmap_generation_failed", error=str(e))
            return {
                "roadmap": [
                    {
                        "skill": skill,
                        "priority": idx + 1,
                        "current_level": "beginner",
                        "target_level": "intermediate",
                        "learning_path": [],
                        "resources": [],
                        "practice_project": "Build a small project applying this skill.",
                        "estimated_hours": 40,
                        "milestones": [],
                    }
                    for idx, skill in enumerate(skills_to_acquire)
                ],
                "total_estimated_weeks": max(1, len(skills_to_acquire)),
                "recommended_order": skills_to_acquire,
            }
