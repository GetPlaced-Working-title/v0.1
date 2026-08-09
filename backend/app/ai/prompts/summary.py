"""Prompt templates for candidate summary and interview questions."""

CANDIDATE_SUMMARY_PROMPT = """
You are a hiring expert. Generate a recruiter-facing summary of a candidate based on their complete evidence-backed profile.

## Candidate Profile:
{profile}

## Requirements:
1. 2-3 paragraphs maximum.
2. Lead with the strongest verified evidence, not self-reported claims.
3. Separate what is PROVEN from what is CLAIMED.
4. Mention evidence confidence level.
5. Highlight top 3 strengths backed by evidence.
6. Note any red flags or gaps that need verification.
7. Suggest what types of roles this candidate is best suited for.
8. Include a "Quick Read" section: 3 bullet points a recruiter can scan in 5 seconds.

## Output Schema
Return JSON:
{
  "quick_read": ["...", "...", "..."],
  "summary": "...",
  "proven_evidence": [{"claim": "...", "evidence": "...", "confidence": "high"}],
  "claimed_but_unverified": ["..."],
  "recommended_roles": ["..."],
  "evidence_confidence": "medium",
  "interview_focus_areas": ["...", "..."]
}
"""
