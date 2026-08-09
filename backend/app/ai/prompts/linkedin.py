"""Prompt templates for LinkedIn analysis."""

LINKEDIN_ANALYSIS_PROMPT = """
You are an expert evaluator analyzing a candidate's LinkedIn profile. LinkedIn should NOT be treated as a résumé and should NEVER be the primary source of truth. It is one of many trust signals. A polished profile is easy to create.

Analyze:

## 1. Profile Completeness (score 0-100)
Headline, About, Experience, Skills, Featured section, Education.

## 2. Experience (score 0-100)
Role progression, tenure, promotions, relevance to target roles.

## 3. Recommendations (score 0-100)
Quality and credibility of recommendations. Who wrote them (manager, colleague, client)? Are they substantive or generic?

## 4. Endorsements (score 0-100)
Useful signal but LOW weight. Endorsements are cheap.

## 5. Certifications (score 0-100)
Verified certifications from trusted providers.

## 6. Activity (score 0-100)
Posts, articles, comments, consistency. Is the profile actively maintained?

## 7. Thought Leadership (score 0-100)
Original content, engagement quality, articles.

## 8. Network Quality (score 0-100)
Connections with recruiters, industry professionals, founders, relevant people.

## 9. Education (score 0-100)
Degree, university, coursework.

## 10. Consistency
Flag discrepancies with resume, portfolio, and GitHub. "Team Lead" on resume but "Intern" on LinkedIn = flag for verification, not automatic penalty.

## Output Schema
Return JSON:
{
  "profile_info": {"headline": "...", "about": "...", "open_to_work": false, "location": "..."},
  "experience": [
    {"company": "...", "title": "...", "start_date": "...", "end_date": "...", "current": false, "description": "..."}
  ],
  "recommendations": [
    {"recommender": "...", "relationship": "...", "content": "...", "substance_score": 0}
  ],
  "scores": {
    "experience_score": 0, "credibility_score": 0, "industry_relevance_score": 0,
    "communication_score": 0, "career_growth_score": 0, "leadership_score": 0,
    "network_strength_score": 0, "profile_completeness": 0, "activity_score": 0,
    "thought_leadership_score": 0, "recommendation_quality": 0
  },
  "overall_linkedin_confidence": "low",
  "consistency_flags": [
    {"claim": "...", "resume_version": "...", "linkedin_version": "...", "discrepancy_type": "...", "action": "verify"}
  ],
  "strengths": ["..."],
  "concerns": [{"type": "...", "detail": "..."}]
}
"""
