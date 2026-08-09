# AI Talent Router

## Mission

Build an AI-powered hiring platform that understands candidates from evidence instead of keywords.

## What the system analyzes

- Resume
- GitHub
- Portfolio
- LinkedIn Export
- Projects
- Certificates
- Recommendation Letters
- Work History
- Skill Demonstration Videos

The AI produces a complete candidate profile. Companies never browse thousands of resumes.

## Matching Flow

```
Job → Embedding → Vector Search → Top Candidates → AI Reranker → Recruiter Dashboard
```

---

## Tech Stack

### Frontend
- Next.js 15
- TypeScript
- Tailwind CSS
- shadcn/ui

### Backend
- FastAPI
- SQLAlchemy
- Pydantic
- Alembic (migrations)

### Database
- PostgreSQL

### Cache
- Redis

### Vector DB
- Qdrant

### Search
- Meilisearch

### Storage
- Cloudflare R2

### Queue
- Celery

### Deployment
- Docker + Docker Compose
- Coolify

---

## AI Stack

### Gemini Flash Lite
Used for all text analysis:
- Resume Parsing
- Portfolio Analysis
- GitHub Analysis
- LinkedIn Analysis
- Project Analysis
- Certificate Analysis
- Recommendation Analysis
- Work History Analysis
- Candidate Summary

### Gemini Video
Used for video analysis:
- Communication
- Confidence
- Technical Knowledge
- Problem Solving
- Authenticity
- Leadership

### Embeddings
- Gemini Embeddings → stored in Qdrant

---

## AI Principles

1. Never call AI twice for the same input — always cache.
2. Always produce structured JSON.
3. Never store natural language if structured data can be stored.
4. Never run expensive inference during recruiter search.
5. Inference happens only during profile creation or update.

---

## Matching Pipeline

```
Candidate → Embedding → Qdrant → Top 50 → Gemini Rerank → Top 10
```

---

## Coding Standards

- Strict TypeScript (frontend)
- Fully typed Python (backend)
- Modular architecture
- Repository pattern
- Clean Architecture
- No duplicated logic
- Every feature must be documented
- Tests for business logic
- Environment variables for config
- Never hardcode secrets

---

## Project Structure

See `docs/architecture.md` for the full folder tree.

## Commands

```bash
# Start all services
docker compose up -d

# Run backend
cd backend && uvicorn app.main:app --reload

# Run frontend
cd frontend && npm run dev

# Run tests
cd backend && pytest
cd frontend && npm test
```

---

## Docs

- `docs/architecture.md` — folder structure and responsibilities
- `docs/database.md` — ER diagram and SQL schema
- `docs/api.md` — REST API endpoints
- `docs/ai-pipeline.md` — AI analysis pipeline design
- `docs/roadmap.md` — milestones
- `docs/prompts.md` — AI prompt templates
- `docs/scoring.md` — candidate scoring logic
- `docs/ui.md` — UI/UX design notes
