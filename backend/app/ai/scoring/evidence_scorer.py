"""Evidence confidence scoring."""

from __future__ import annotations

from enum import Enum


class EvidenceConfidence(str, Enum):
    """Confidence levels for a claim based on supporting evidence."""

    NONE = "none"
    LOW = "low"           # Resume only
    MEDIUM = "medium"     # Resume + one source
    HIGH = "high"         # Resume + multiple sources
    VERY_HIGH = "very_high"  # Resume + verified production evidence


# Source reliability weights (0-1) — resume carries LESS weight
SOURCE_WEIGHTS = {
    "resume": 0.4,
    "linkedin": 0.5,
    "work_history": 0.7,
    "certificate_verified": 0.6,
    "certificate_unverified": 0.3,
    "recommendation": 0.5,
    "video": 0.9,
    "github": 0.9,
    "portfolio_live": 0.9,
    "portfolio_static": 0.6,
    "project_production": 1.0,
    "project_personal": 0.6,
    "assessment": 0.95,
}


def calculate_confidence(sources: list[str]) -> EvidenceConfidence:
    """Calculate evidence confidence from a list of evidence source keys."""
    if not sources:
        return EvidenceConfidence.NONE

    # Unique non-resume sources
    external = [s for s in sources if s != "resume"]
    has_production = any(s in ("project_production", "github", "portfolio_live") for s in sources)
    has_assessment = "assessment" in sources

    if has_assessment and has_production:
        return EvidenceConfidence.VERY_HIGH
    if has_production and len(external) >= 2:
        return EvidenceConfidence.HIGH
    if has_production or len(external) >= 2:
        return EvidenceConfidence.MEDIUM
    if external:
        return EvidenceConfidence.MEDIUM
    return EvidenceConfidence.LOW


def weight_for_source(source: str) -> float:
    """Get the reliability weight for a source."""
    return SOURCE_WEIGHTS.get(source, 0.5)


def composite_score(
    scores: dict[str, float],
    weights: dict[str, float],
) -> float:
    """Compute a weighted composite score (0-100)."""
    if not scores:
        return 0.0
    total_weight = 0.0
    total = 0.0
    for key, score in scores.items():
        w = weights.get(key, 1.0)
        total += score * w
        total_weight += w
    if total_weight == 0:
        return 0.0
    return round(total / total_weight, 1)


def clamp_score(value: float, low: float = 0, high: float = 100) -> float:
    """Clamp a score to [low, high]."""
    return max(low, min(high, value))