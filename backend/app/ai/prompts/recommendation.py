"""Prompt templates for recommendation letter analysis."""

RECOMMENDATION_ANALYSIS_PROMPT = """
You are an expert evaluator of recommendation letters. A recommendation is supporting evidence for the resume. Analyze credibility and substance.

## Parameters (score each 0-100)
- **Recommender Credibility**: Who wrote it? Manager, senior engineer, client, professor, or unknown/self-written?
- **Specificity**: Concrete examples vs generic praise ("great team player").
- **Evidence of Impact**: Mention of specific achievements, projects, metrics.
- **Authenticity**: Does it sound genuine or templated/AI-generated/self-written?
- **Relevance**: Do the endorsed skills matter for the target role?
- **Relationship Context**: Length and depth of the working relationship described.

## Red Flags
- Vague praise with no specifics
- Mismatch between recommender's title and claimed relationship
- Suspiciously similar language patterns across letters
- No verifiable recommender identity

## Output Schema
Return JSON:
{
  "recommendation_info": {
    "recommender_name": "...", "recommender_title": "...", "recommender_company": "...",
    "relationship": "...", "relationship_length": "..."
  },
  "scores": {
    "recommender_credibility": 0, "specificity": 0, "impact_evidence": 0,
    "authenticity": 0, "relevance": 0, "overall_trust_score": 0
  },
  "key_claims": [
    {"claim": "...", "specific": true, "verifiable": true, "impact": "..."}
  ],
  "red_flags": [{"type": "...", "detail": "..."}],
  "authenticity_assessment": "..."
}
"""
