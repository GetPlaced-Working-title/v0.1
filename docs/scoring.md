# Scoring Logic

> How candidates are scored and ranked.

## Score Types

### Per-Evidence Scores
Each analyzer produces scores specific to its evidence type:

- **Resume**: experience_quality, achievement_quality, resume_quality, ats_compatibility
- **GitHub**: technical_depth, code_quality, consistency, contribution_frequency
- **Portfolio**: design_quality, project_quality, technical_sophistication
- **Video**: communication, confidence, technical_knowledge, authenticity
- **Certificate**: issuer_credibility, difficulty_level, relevance
- **Work History**: impact, progression, responsibility_growth

### Aggregate Scores
The `ProfileBuilder` merges all per-evidence scores using weighted averaging:

1. For each score dimension, take the weighted average across all sources
2. Weights are based on source reliability (see AI Pipeline doc)
3. Overall profile strength = average of all aggregate scores

## Evidence Confidence
Determined by which sources have contributed analysis:

- **none**: No sources analyzed
- **low**: Only resume analyzed
- **medium**: GitHub or work history present
- **high**: Portfolio or video present
- **very_high**: Multiple verified sources with cross-consistency

## Skill Confidence
Each skill has a confidence level based on evidence sources:

- **resume_mention**: Only mentioned in resume (lowest)
- **github_verified**: Code in GitHub demonstrates the skill
- **portfolio_verified**: Portfolio projects show the skill
- **assessment_verified**: Certificate or test verifies the skill
- **production_verified**: Production work history confirms the skill (highest)

## Consistency Checks
The `ConsistencyChecker` compares claims across sources:

- Resume claims vs GitHub activity
- Stated skills vs demonstrated skills
- Experience timeline consistency
- Education claims vs certificates

Inconsistencies are flagged, not silently corrected.

## Red Flag Detection
The `RedFlagDetector` identifies potential concerns:

- Skills listed but no evidence in any source
- Experience gaps without explanation
- Inconsistent dates across sources
- Overly broad skill claims without depth
- AI-generated code detection in GitHub
