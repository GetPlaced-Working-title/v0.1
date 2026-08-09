# AI Prompt Templates

> All prompts used for AI analysis. Located in `backend/app/ai/prompts/`.

## Design Principles

1. Always request structured JSON output
2. Include explicit score ranges (0.0 to 1.0)
3. Ask for evidence-based reasoning, not opinions
4. Include skill extraction in every analysis
5. Flag uncertainty rather than guessing

## Prompt Files

| File | Used By | Purpose |
|------|---------|---------|
| `resume.py` | ResumeAnalyzer | Parse and score resume content |
| `github.py` | GitHubAnalyzer | Analyze code quality and engineering practices |
| `portfolio.py` | PortfolioAnalyzer | Evaluate design and project quality |
| `linkedin.py` | LinkedInAnalyzer | Analyze career trajectory |
| `project.py` | ProjectAnalyzer | Evaluate individual projects |
| `video.py` | VideoAnalyzer | Analyze communication and knowledge |
| `certificate.py` | CertificateAnalyzer | Verify and score certificates |
| `recommendation.py` | RecommendationAnalyzer | Evaluate recommendation credibility |
| `work_history.py` | WorkHistoryAnalyzer | Analyze work experience |
| `profile_builder.py` | ProfileBuilder | Aggregate all analyses |
| `reranker.py` | RerankerService | Rerank candidates for a job |
| `red_flag.py` | RedFlagDetector | Detect inconsistencies |
| `skill_gap.py` | SkillGapGenerator | Identify missing skills |
| `summary.py` | SummaryGenerator | Generate candidate summary |
| `interview_questions.py` | InterviewGenerator | Generate targeted questions |

## Output Format

All analyzers return JSON with this structure:

```json
{
  "scores": {
    "dimension_name": 0.75
  },
  "skills": [
    {
      "name": "Python",
      "category": "programming",
      "confidence": "high"
    }
  ],
  "summary": "Brief analysis summary",
  "details": {}
}
```
