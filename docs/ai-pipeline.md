# AI Pipeline

> How the AI analysis system works.

## Architecture

```
Evidence Upload → Celery Task → Analyzer → Gemini AI → Cache → Structured Storage
                                     ↓
                              Profile Builder → Aggregated Scores → Embedding → Qdrant
```

## Principles

1. **Never call AI twice** — SHA256 hash of (analyzer_type + content) cached in `ai_analysis_cache`
2. **Structured JSON only** — All Gemini responses use `response_mime_type: application/json`
3. **Never store raw AI output** — Always parse into typed model fields
4. **No inference at search time** — All AI runs during profile creation/update
5. **Resume weighted below verified evidence** — Self-reported data carries less weight

## Analyzers

| Analyzer | Model | Input | Output |
|----------|-------|-------|--------|
| Resume | Flash Lite | Resume text | Skills, experience, education, scores |
| GitHub | Flash Lite | Profile + repos | Code quality, patterns, skill verification |
| Portfolio | Flash Lite | URL content | Design quality, project depth |
| LinkedIn | Flash Lite | Export data | Career trajectory, consistency |
| Project | Flash Lite | Description + links | Complexity, technology depth |
| Certificate | Flash Lite | Name + issuer + URL | Verification, difficulty, credibility |
| Work History | Flash Lite | Role + achievements | Impact, growth, responsibility |
| Recommendation | Flash Lite | Letter content | Specificity, credibility |
| Video | Gemini Video | Video file | Communication, confidence, knowledge |

## Scoring

### Evidence Confidence Levels

- **none** — No evidence uploaded
- **low** — Resume only
- **medium** — GitHub or work history analyzed
- **high** — Portfolio or video analyzed
- **very_high** — Multiple verified sources with consistency

### Source Priority Weights

| Source | Weight |
|--------|--------|
| Portfolio | 0.9 |
| Video | 0.9 |
| GitHub | 0.9 |
| Work History | 0.8 |
| LinkedIn | 0.6 |
| Certificate | 0.6 |
| Recommendation | 0.5 |
| Resume | 0.4 |

## Matching Pipeline

```
Job Description → Embedding → Qdrant Vector Search → Top 50
                                                          ↓
                                         Gemini Reranker → Top 10 → Store in job_matches
```

Steps:
1. Generate job embedding from title + description + skills
2. Vector search against all candidate embeddings in Qdrant
3. Return top 50 by cosine similarity
4. AI reranks top 50 considering full candidate profiles
5. Store final top 10 matches with scores, strengths, gaps
