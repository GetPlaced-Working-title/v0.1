"""Interview question generator."""

from __future__ import annotations

import json
from typing import Any

from app.ai.client import get_gemini_client
from app.ai.prompts.interview_questions import INTERVIEW_QUESTIONS_PROMPT
from app.core.logging import get_logger

logger = get_logger(__name__)


class InterviewQuestionGenerator:
    """Generates evidence-based, personalized interview questions."""

    def __init__(self) -> None:
        self._client = get_gemini_client()

    async def generate(
        self,
        job: dict[str, Any],
        profile: dict[str, Any],
    ) -> dict[str, Any]:
        """Generate interview questions for a candidate against a job."""
        prompt = INTERVIEW_QUESTIONS_PROMPT
        prompt = prompt.replace("{job_title}", job.get("title", "Unknown"))
        prompt = prompt.replace("{job_description}", (job.get("description") or "")[:5000])
        prompt = prompt.replace("{required_skills}", ", ".join(job.get("required_skills", []) or []))
        prompt = prompt.replace("{profile}", json.dumps(profile, default=str)[:30000])

        try:
            return await self._client.analyze_text(prompt=prompt, content="")
        except Exception as e:
            logger.error("interview_questions_failed", error=str(e))
            return self._fallback(job, profile)

    @staticmethod
    def _fallback(job: dict[str, Any], profile: dict[str, Any]) -> dict[str, Any]:
        """Fallback generic questions when the AI is unavailable."""
        skills = ", ".join((job.get("required_skills") or [])[:5])
        return {
            "interview_questions": [
                {
                    "question": f"Walk me through your most relevant experience for {job.get('title', 'this role')}.",
                    "category": "role_fit",
                    "rationale": "Establishes baseline fit for the role.",
                    "expected_depth": "intermediate",
                    "follow_ups": ["What was your specific contribution?", "What would you do differently?"],
                    "targets_claim": "General experience",
                },
                {
                    "question": f"Which of these skills do you use most day-to-day: {skills or 'your listed skills'}?",
                    "category": "verification",
                    "rationale": "Verifies claimed skills against demonstrated usage.",
                    "expected_depth": "intermediate",
                    "follow_ups": ["Give me a concrete example."],
                    "targets_claim": "Skill list",
                },
            ],
            "priority_order": ["First ask the role-fit question, then verification."],
            "interview_strategy": (
                "Probe claims where evidence confidence is low. Ask for concrete examples "
                "and trade-offs rather than definitions."
            ),
        }
