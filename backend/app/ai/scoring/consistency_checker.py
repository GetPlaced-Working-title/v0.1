"""Consistency checker — compares claims across evidence sources."""

from __future__ import annotations

from typing import Any

from app.core.logging import get_logger

logger = get_logger(__name__)


class ConsistencyChecker:
    """Compares data across sources and flags discrepancies (without auto-penalizing)."""

    def __init__(self) -> None:
        self.flags: list[dict[str, Any]] = []

    def compare_role_titles(
        self,
        claims: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """Compare role titles across sources for the same company/timeframe."""
        flags: list[dict[str, Any]] = []
        grouped: dict[str, list[dict[str, Any]]] = {}

        for claim in claims:
            # Normalize company name
            company = (claim.get("company") or "").strip().lower()
            key = f"{company}|{claim.get('start_date', '')}"
            if key not in grouped:
                grouped[key] = []
            grouped[key].append(claim)

        for key, entries in grouped.items():
            if len(entries) < 2:
                continue
            titles = {e.get("title") for e in entries if e.get("title")}
            if len(titles) > 1:
                flags.append(
                    {
                        "type": "title_discrepancy",
                        "company": key.split("|")[0],
                        "titles": list(titles),
                        "sources": [e.get("source") for e in entries],
                        "severity": "medium",
                        "action": "verify",
                        "detail": (
                            f"Same company/role listed with different titles across sources: "
                            f"{', '.join(str(t) for t in titles)}"
                        ),
                    }
                )
        self.flags.extend(flags)
        return flags

    def verify_date_ranges(
        self,
        claims: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """Check for date discrepancies across sources."""
        flags: list[dict[str, Any]] = []
        by_company: dict[str, list[dict[str, Any]]] = {}

        for claim in claims:
            company = (claim.get("company") or "").strip().lower()
            by_company.setdefault(company, []).append(claim)

        for company, entries in by_company.items():
            if len(entries) < 2:
                continue
            start_dates = {e.get("start_date") for e in entries if e.get("start_date")}
            end_dates = {e.get("end_date") for e in entries if e.get("end_date")}

            if len(start_dates) > 1 or len(end_dates) > 1:
                flags.append(
                    {
                        "type": "date_discrepancy",
                        "company": company,
                        "start_dates": list(start_dates),
                        "end_dates": list(end_dates),
                        "sources": [e.get("source") for e in entries],
                        "severity": "medium",
                        "action": "verify",
                        "claim": f"Date ranges conflict for {company}",
                    }
                )
        self.flags.extend(flags)
        return flags

    def verify_skill_evidence(
        self,
        resume_skills: list[str],
        verified_skills: list[str],
    ) -> list[dict[str, Any]]:
        """Flag skills claimed in resume but with no external verification."""
        flags: list[dict[str, Any]] = []
        claimed_set = {s.lower() for s in resume_skills if s}
        verified_set = {s.lower() for s in verified_skills if s}

        unverified = claimed_set - verified_set
        if unverified:
            flags.append(
                {
                    "type": "unverified_skills",
                    "skills": sorted(unverified),
                    "severity": "low",
                    "action": "verify_on_github_or_portfolio",
                    "claim": (
                        f"{len(unverified)} skills claimed but not verified externally: "
                        f"{', '.join(sorted(unverified)[:10])}"
                    ),
                    "sources": ["resume"],
                }
            )
        self.flags.extend(flags)
        return flags

    def check_experience_claim_matches_evidence(
        self,
        claimed_years: float | None,
        github_account_age_days: int | None,
    ) -> list[dict[str, Any]]:
        """Flag when claimed years of experience contradict GitHub history."""
        if not claimed_years or not github_account_age_days:
            return []

        years_from_github = max(0, github_account_age_days / 365.25)
        # Soft heuristic: flag only if GitHub account is much younger than claimed experience
        # in a field where GitHub should show long history
        if claimed_years > years_from_github + 2:
            flag = {
                "type": "experience_mismatch",
                "claim": f"{claimed_years} claimed years of experience",
                "evidence": f"GitHub account only {years_from_github:.1f} years old",
                "severity": "medium",
                "action": "verify",
                "sources": ["resume", "github"],
            }
            self.flags.append(flag)
            return [flag]
        return []

    def get_all_flags(self) -> list[dict[str, Any]]:
        """Return all collected flags."""
        return self.flags
