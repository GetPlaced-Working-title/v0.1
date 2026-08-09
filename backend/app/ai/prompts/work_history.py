"""Prompt templates for work history analysis."""

WORK_HISTORY_ANALYSIS_PROMPT = """
You are an expert career evaluator analyzing a candidate's work history. Don't just count years — analyze the trajectory.

## Parameters (score each 0-100)
- **Relevance**: How closely does experience align with the target role?
  - Business Analyst applying for Business Analyst: High
  - Data Analyst applying for Business Analyst: Medium
  - Sales Executive applying for Business Analyst: Low
- **Career Progression**: Growth in responsibilities over time.
  - Intern → Associate → Analyst → Senior Analyst (strong)
  - Analyst → Analyst → Analyst (weak)
- **Stability**: Average tenure. Do NOT penalize internships or contract work.
- **Responsibility Growth**: Increasing scope over time.
  - "Assisted with reporting" → "Managed reporting" → "Led reporting automation" → "Managed a reporting team"
- **Leadership Evidence**: Managed interns, led projects, mentored teammates, coordinated stakeholders, owned deliverables.

## Output Schema
Return JSON:
{
  "work_history": [
    {"company": "...", "title": "...", "start_date": "...", "end_date": "...", "current": false,
     "employment_type": "...", "role_relevance": "high", "description": "...",
     "achievements": [{"text": "...", "quantified": true, "impact": "..."}]}
  ],
  "scores": {
    "experience_relevance": 0, "career_progression": 0, "stability": 0,
    "responsibility_growth": 0, "leadership_evidence": 0, "experience_quality": 0
  },
  "career_timeline": {
    "progression_trend": "intern -> associate -> analyst -> senior",
    "trajectory_type": "ascending",  # ascending, flat, mixed, unclear
    "average_tenure_months": 0,
    "job_hopping_detected": false,
    "gaps_detected": [{"start": "...", "end": "...", "months": 0}]
  },
  "strengths": ["..."],
  "concerns": [{"type": "...", "detail": "..."}]
}
"""
