"""Profile builder — aggregates all analyses into a candidate knowledge graph."""

from __future__ import annotations

from typing import Any

from app.ai.scoring.evidence_scorer import calculate_confidence, clamp_score
from app.core.logging import get_logger

logger = get_logger(__name__)

# How much each evidence source should influence aggregate scoring.
# Resume deliberately carries LESS weight — it is self-reported.
_SOURCE_PRIORITY = {
    "profile": 1.0,
    "portfolio": 0.9,
    "video": 0.9,
    "github": 0.9,
    "work_history": 0.8,
    "linkedin": 0.6,
    "certificate": 0.6,
    "recommendation": 0.5,
    "resume": 0.4,
}


class ProfileBuilder:
    """Combines all analyzer outputs into a single candidate knowledge graph.

    Principles enforced:
    - Never assign a single universal score — every item carries value + evidence + relevance.
    - A resume is a starting hypothesis; weight it below verified evidence.
    - Flag inconsistencies rather than silently choosing one source.
    """

    def __init__(self) -> None:
        self._scores: dict[str, float] = {}
        self._score_source: dict[str, str] = {}
        self._skills: dict[str, dict[str, Any]] = {}

    def add_analysis(
        self,
        source: str,
        analysis: dict[str, Any],
    ) -> None:
        """Merge an analysis from one evidence source into the graph."""
        priority = _SOURCE_PRIORITY.get(source, 0.5)
        scores = analysis.get("scores", {}) or {}

        for key, value in scores.items():
            if not isinstance(value, (int, float)):
                continue
            if key in self._scores:
                # Weighted average by source priority
                existing_priority = _SOURCE_PRIORITY.get(self._score_source.get(key, ""), 0.5)
                combined_priority = existing_priority + priority
                self._scores[key] = (
                    (self._scores[key] * existing_priority + value * priority)
                    / combined_priority
                )
            else:
                self._scores[key] = float(value)
                self._score_source[key] = source

        # Merge skills
        for skill in analysis.get("skills", []) or []:
            name = (skill.get("name") or "").strip().lower()
            if not name:
                continue
            category = skill.get("category")
            display_name = skill.get("name")
            if name not in self._skills:
                self._skills[name] = {
                    "name": display_name or name,
                    "category": category,
                    "confidence": "none",
                    "verified": False,
                    "sources": [],
                }
            self._skills[name]["sources"].append(source)

    def build(self) -> dict[str, Any]:
        """Produce the final aggregated profile."""
        scores_values = list(self._scores.values())
        overall = clamp_score(sum(scores_values) / max(1, len(scores_values)))

        return {
            "aggregate_scores": self._scores,
            "skills_graph": self._finalize_skills(),
            "overall_profile_strength": overall,
            "evidence_confidence": self._determine_confidence(),
        }

    def _finalize_skills(self) -> list[dict[str, Any]]:
        """Assign confidence per skill based on its evidence sources."""
        result: list[dict[str, Any]] = []
        for _name, skill in self._skills.items():
            sources = skill.pop("sources", [])
            confidence = calculate_confidence(sources)
            skill["confidence"] = confidence.value
            skill["verified"] = confidence in ("high", "very_high")
            skill["evidence_sources"] = sources
            result.append(skill)
        return result

    def _determine_confidence(self) -> str:
        """Compute overall evidence confidence from which sources informed the profile."""
        if not self._scores:
            return "none"
        if "video" in self._score_source.values() or "portfolio" in self._score_source.values():
            return "high"
        if "github" in self._score_source.values() or "work_history" in self._score_source.values():
            return "medium"
        return "low"
