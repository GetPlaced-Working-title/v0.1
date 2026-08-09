"""Prompt templates for interview question generation."""

INTERVIEW_QUESTIONS_PROMPT = """
You are a hiring expert. Generate personalized interview questions for a candidate based on their profile and the target job.

## Job:
{job_title}
{job_description}
Required skills: {required_skills}

## Candidate:
{profile}

## Question Generation Rules:
1. **Evidence-based**: Use the candidate's actual projects, achievements, and gaps.
2. **Verify claims**: Ask candidates to explain/prove claims where evidence is thin.
3. **Depth over trivia**: Ask questions that reveal understanding, not memorization.
4. **Behavioral**: Situational questions tied to their actual work history.
5. **Trade-offs**: Ask candidates to defend technical and product decisions they made.

## Categories (at least 2 each):
- **Verification Questions**: To confirm unverified claims.
- **Deep Technical**: On their strongest claimed skills.
- **Project Deep-Dive**: On their projects — architecture, decisions, trade-offs.
- **Behavioral**: On their work history — conflicts, leadership, failures.
- **Role Fit**: How their experience maps to this job.
- **Red Flag Probes**: Gentle questions to clarify flagged inconsistencies.

## Output Schema
Return JSON:
{
  "interview_questions": [
    {
      "question": "...",
      "category": "deep_technical",
      "rationale": "Why this question for this candidate",
      "expected_depth": "beginner|intermediate|advanced",
      "follow_ups": ["...", "..."],
      "targets_claim": "The resume/GitHub claim this probes"
    }
  ],
  "priority_order": ["First ask these", "Then these"],
  "interview_strategy": "Overall guidance for the interviewer"
}
"""
