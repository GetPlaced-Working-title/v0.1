"""Prompt templates for skill gap analysis and learning roadmap."""

SKILL_GAP_ANALYSIS_PROMPT = """
You are a skill gap analyst. Compare a candidate's verified skill set against a target job's requirements.

## Job Requirements:
{job_requirements}

## Candidate Verified Skills:
{candidate_skills}

For each required skill, determine:
- **Status**: has (verified), claims (unverified), missing, adjacent
- **Gap severity**: none, minor, moderate, major
- **Mitigation evidence**: existing skills that partially cover this gap

## Output Schema
Return JSON:
{
  "skill_gaps": [
    {"skill": "...", "status": "missing", "gap_severity": "major", "importance": "required",
     "mitigation": "...", "suggested_evidence": "..."}
  ],
  "overall_gap_score": 0,  # 100 = no gaps, 0 = many major gaps
  "summary": "..."
}
"""

LEARNING_ROADMAP_PROMPT = """
You are a learning advisor. Create a personalized learning roadmap for a candidate to close skill gaps for a target role.

## Target Role:
{target_role}

## Skills to acquire:
{skills_to_acquire}

## Current background:
{candidate_background}

Create a structured, realistic roadmap:
- Ordered by priority (highest-impact skills first)
- Each item: skill, learning path, resources, estimated time, practice project, milestone
- Project-based learning prioritized over passive consumption

## Output Schema
Return JSON:
{
  "roadmap": [
    {
      "skill": "...",
      "priority": 1,
      "current_level": "...",
      "target_level": "...",
      "learning_path": ["...", "..."],
      "resources": [{"name": "...", "url": "...", "type": "course|docs|book|video|project"}],
      "practice_project": "...",
      "estimated_hours": 0,
      "milestones": [{"week": 1, "goal": "..."}]
    }
  ],
  "total_estimated_weeks": 0,
  "recommended_order": ["..."]
}
"""
