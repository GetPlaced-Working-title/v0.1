"""Red flag detector.

Rules-based detection of fraud indicators across the candidate profile.
AI-based deep analysis lives in the analyst; this handles deterministic checks.
"""

from __future__ import annotations

from typing import Any

from app.ai.prompts.red_flag import RED_FLAG_DETECTION_PROMPT
from app.ai.scoring.evidence_scorer import clamp_score
from app.core.logging import get_logger

logger = get_logger(__name__)


class RedFlagDetector:
    """Deterministic red flag detection + AI deep analysis."""

    def __init__(self) -> None:
        self.flags: list[dict[str, Any]] = []

    def check_suspicious_quantifications(
        self,
        achievements: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """Flag achievements with implausible or overly round metrics."""
        flags: list[dict[str, Any]] = []
        for achievement in achievements or []:
            text = achievement.get("text", "")
            metric = achievement.get("metric")
            if metric is None:
                continue
            # Heuristics for suspicious numbers
            suspicious_phrases = [
                "99.9%", "100%", "10x", "infinity", "millions of dollars",
                "10,000%", "-100%",
            ]
            lowered = text.lower()
            if metric in suspicious_phrases or any(  # noqa: SIM118
                p in lowered for p in suspicious_phrases
            ):
                flags.append(
                    {
                        "type": "suspicious_quantification",
                        "claim": text,
                        "metric": metric,
                        "severity": "medium",
                        "action": "verify_metric_with_source",
                    }
                )
        self.flags.extend(flags)
        return flags

    def check_duplicate_content(
        self,
        items: list[dict[str, Any]],
        content_key: str = "description",
    ) -> list[dict[str, Any]]:
        """Flag near-identical descriptions across projects or roles."""
        flags: list[dict[str, Any]] = []
        seen: dict[str, list[str]] = {}

        for item in items or []:
            content = (item.get(content_key) or "").strip()
            if not content:
                continue
            # Simple normalized signature
            sig = " ".join(content.lower().split())[:200]
            if sig in seen:
                seen[sig].append(item.get("title") or item.get("company") or "unknown")
            else:
                seen[sig] = [(item.get("title") or item.get("company") or "unknown")]

        for sig, owners in seen.items():
            if len(owners) > 1:
                flags.append(
                    {
                        "type": "duplicate_content",
                        "items": owners,
                        "severity": "low",
                        "action": "inspect",
                        "detail": f"Near-identical {content_key} across: {', '.join(owners)}",
                    }
                )
        self.flags.extend(flags)
        return flags

    def detect_old_claims(
        self,
        items: list[dict[str, Any]],
        date_key: str,
        current_year: int = 2026,
        threshold_years: int = 5,
    ) -> list[dict[str, Any]]:
        """Flag skills/projects with no recent activity."""
        flags: list[dict[str, Any]] = []
        for item in items or []:
            year = self._extract_year(item.get(date_key))
            if year and (current_year - year) > threshold_years:
                flags.append(
                    {
                        "type": "recency_gap",
                        "claim": item,
                        "last_active": str(year),
                        "severity": "low",
                        "action": "note",
                    }
                )
        self.flags.extend(flags)
        return flags

    def get_flags(self) -> list[dict[str, Any]]:
        """Return all deterministic flags."""
        return list(self.flags)

    def clear(self) -> None:
        """Reset all flags."""
        self.flags = []

    @staticmethod
    def _extract_year(value: Any) -> int | None:
        """Extract a year from a date value."""
        if value is None:
            return None
        if isinstance(value, int):
            return value
        text = str(value)
        # Look for a 4-digit year
        import re

        match = re.search(r"(19|20)\d{2}", text)
        if match:
            return int(match.group(0))
        return None