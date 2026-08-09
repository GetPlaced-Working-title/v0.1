# Architecture

> Full folder structure and module responsibilities.

## Folder Tree

```
talent-ai/
├── backend/
│   ├── alembic/
│   │   ├── versions/
│   │   ├── env.py
│   │   └── alembic.ini
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                        # FastAPI app factory
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── config.py                  # Pydantic Settings
│   │   │   ├── database.py                # SQLAlchemy engine + session
│   │   │   ├── redis.py                   # Redis client
│   │   │   ├── qdrant.py                  # Qdrant client
│   │   │   ├── meilisearch.py             # Meilisearch client
│   │   │   ├── storage.py                 # Cloudflare R2 (S3-compatible)
│   │   │   ├── celery_app.py              # Celery configuration
│   │   │   ├── security.py                # Auth helpers (Clerk verification)
│   │   │   ├── exceptions.py              # Custom exceptions
│   │   │   ├── logging.py                 # Structured logging
│   │   │   └── dependencies.py            # FastAPI dependency injection
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── base.py                    # Base model with timestamps, soft delete
│   │   │   ├── user.py                    # Users, roles
│   │   │   ├── company.py                 # Companies
│   │   │   ├── job.py                     # Job postings
│   │   │   ├── candidate.py               # Candidate profiles
│   │   │   ├── resume.py                  # Resume records + analysis
│   │   │   ├── github_profile.py          # GitHub analysis
│   │   │   ├── portfolio.py               # Portfolio analysis
│   │   │   ├── linkedin.py                # LinkedIn export analysis
│   │   │   ├── project.py                 # Project records + analysis
│   │   │   ├── certificate.py             # Certificates + analysis
│   │   │   ├── video.py                   # Skill demo videos + analysis
│   │   │   ├── recommendation.py          # Recommendation letters + analysis
│   │   │   ├── work_history.py            # Work history + analysis
│   │   │   ├── skill.py                   # Skills with evidence tracking
│   │   │   ├── embedding.py               # Embedding records
│   │   │   ├── ai_score.py                # AI-generated scores
│   │   │   ├── job_match.py               # Job–candidate matches
│   │   │   ├── notification.py            # Notifications
│   │   │   └── audit_log.py               # Audit trail
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── company.py
│   │   │   ├── job.py
│   │   │   ├── candidate.py
│   │   │   ├── resume.py
│   │   │   ├── github.py
│   │   │   ├── portfolio.py
│   │   │   ├── linkedin.py
│   │   │   ├── project.py
│   │   │   ├── certificate.py
│   │   │   ├── video.py
│   │   │   ├── recommendation.py
│   │   │   ├── work_history.py
│   │   │   ├── skill.py
│   │   │   ├── search.py
│   │   │   ├── matching.py
│   │   │   └── common.py                  # Pagination, error responses
│   │   ├── repositories/
│   │   │   ├── __init__.py
│   │   │   ├── base.py                    # Generic CRUD base
│   │   │   ├── user.py
│   │   │   ├── company.py
│   │   │   ├── job.py
│   │   │   ├── candidate.py
│   │   │   ├── resume.py
│   │   │   ├── github.py
│   │   │   ├── portfolio.py
│   │   │   ├── project.py
│   │   │   ├── certificate.py
│   │   │   ├── video.py
│   │   │   ├── skill.py
│   │   │   └── job_match.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── company.py
│   │   │   ├── job.py
│   │   │   ├── candidate.py
│   │   │   ├── resume.py
│   │   │   ├── github.py
│   │   │   ├── portfolio.py
│   │   │   ├── search.py
│   │   │   └── matching.py
│   │   ├── ai/
│   │   │   ├── __init__.py
│   │   │   ├── client.py                  # Gemini API client + caching
│   │   │   ├── prompts/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── resume.py
│   │   │   │   ├── github.py
│   │   │   │   ├── portfolio.py
│   │   │   │   ├── linkedin.py
│   │   │   │   ├── project.py
│   │   │   │   ├── video.py
│   │   │   │   ├── certificate.py
│   │   │   │   ├── recommendation.py
│   │   │   │   ├── work_history.py
│   │   │   │   ├── profile_builder.py
│   │   │   │   ├── reranker.py
│   │   │   │   ├── red_flag.py
│   │   │   │   ├── skill_gap.py
│   │   │   │   ├── summary.py
│   │   │   │   └── interview_questions.py
│   │   │   ├── analyzers/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── base.py                # Base analyzer with caching
│   │   │   │   ├── resume.py
│   │   │   │   ├── github.py
│   │   │   │   ├── portfolio.py
│   │   │   │   ├── linkedin.py
│   │   │   │   ├── project.py
│   │   │   │   ├── video.py
│   │   │   │   ├── certificate.py
│   │   │   │   ├── recommendation.py
│   │   │   │   └── work_history.py
│   │   │   ├── scoring/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── profile_builder.py     # Aggregates all analyses
│   │   │   │   ├── evidence_scorer.py     # Evidence confidence levels
│   │   │   │   ├── consistency_checker.py # Cross-source verification
│   │   │   │   └── red_flag_detector.py
│   │   │   ├── matching/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── embedding.py           # Embedding generation
│   │   │   │   ├── vector_search.py       # Qdrant search
│   │   │   │   ├── keyword_search.py      # Meilisearch search
│   │   │   │   ├── hybrid.py              # Hybrid merger
│   │   │   │   └── reranker.py            # LLM reranker
│   │   │   └── generators/
│   │   │       ├── __init__.py
│   │   │       ├── summary.py             # Candidate summary
│   │   │       ├── interview_questions.py
│   │   │       ├── skill_gap.py
│   │   │       └── learning_roadmap.py
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── candidates.py
│   │   │   ├── companies.py
│   │   │   ├── jobs.py
│   │   │   ├── resumes.py
│   │   │   ├── github.py
│   │   │   ├── portfolios.py
│   │   │   ├── videos.py
│   │   │   ├── certificates.py
│   │   │   ├── search.py
│   │   │   ├── matching.py
│   │   │   ├── admin.py
│   │   │   └── health.py
│   │   ├── tasks/
│   │   │   ├── __init__.py
│   │   │   ├── resume.py                  # Celery: resume processing
│   │   │   ├── github.py                  # Celery: GitHub analysis
│   │   │   ├── portfolio.py               # Celery: portfolio analysis
│   │   │   ├── linkedin.py                # Celery: LinkedIn analysis
│   │   │   ├── video.py                   # Celery: video analysis
│   │   │   ├── certificate.py             # Celery: certificate verification
│   │   │   ├── embedding.py               # Celery: embedding generation
│   │   │   ├── profile.py                 # Celery: profile building
│   │   │   └── matching.py                # Celery: batch matching
│   │   └── middleware/
│   │       ├── __init__.py
│   │       ├── cors.py
│   │       ├── rate_limit.py
│   │       ├── request_id.py
│   │       └── error_handler.py
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── test_analyzers/
│   │   ├── test_services/
│   │   ├── test_routers/
│   │   └── test_matching/
│   ├── requirements.txt
│   ├── requirements-dev.txt
│   ├── Dockerfile
│   ├── .env.example
│   └── pyproject.toml
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx
│   │   │   ├── page.tsx                   # Landing page
│   │   │   ├── (auth)/
│   │   │   │   ├── sign-in/
│   │   │   │   └── sign-up/
│   │   │   ├── candidate/
│   │   │   │   ├── layout.tsx
│   │   │   │   ├── dashboard/
│   │   │   │   ├── profile/
│   │   │   │   ├── resume/
│   │   │   │   ├── projects/
│   │   │   │   ├── certificates/
│   │   │   │   ├── videos/
│   │   │   │   └── settings/
│   │   │   ├── recruiter/
│   │   │   │   ├── layout.tsx
│   │   │   │   ├── dashboard/
│   │   │   │   ├── jobs/
│   │   │   │   ├── candidates/
│   │   │   │   ├── search/
│   │   │   │   ├── matches/
│   │   │   │   └── settings/
│   │   │   └── admin/
│   │   │       ├── layout.tsx
│   │   │       ├── dashboard/
│   │   │       ├── users/
│   │   │       └── analytics/
│   │   ├── components/
│   │   │   ├── ui/                        # shadcn/ui components
│   │   │   ├── layout/
│   │   │   │   ├── header.tsx
│   │   │   │   ├── sidebar.tsx
│   │   │   │   ├── footer.tsx
│   │   │   │   └── nav.tsx
│   │   │   ├── candidate/
│   │   │   │   ├── profile-card.tsx
│   │   │   │   ├── skill-badge.tsx
│   │   │   │   ├── evidence-indicator.tsx
│   │   │   │   ├── score-radar.tsx
│   │   │   │   ├── resume-upload.tsx
│   │   │   │   ├── github-connect.tsx
│   │   │   │   ├── video-upload.tsx
│   │   │   │   └── certificate-upload.tsx
│   │   │   ├── recruiter/
│   │   │   │   ├── job-form.tsx
│   │   │   │   ├── candidate-card.tsx
│   │   │   │   ├── match-score.tsx
│   │   │   │   ├── search-filters.tsx
│   │   │   │   ├── comparison-view.tsx
│   │   │   │   └── shortlist.tsx
│   │   │   └── shared/
│   │   │       ├── loading.tsx
│   │   │       ├── error-boundary.tsx
│   │   │       ├── file-upload.tsx
│   │   │       └── data-table.tsx
│   │   ├── lib/
│   │   │   ├── api/
│   │   │   │   ├── client.ts              # Axios/fetch wrapper
│   │   │   │   ├── candidates.ts
│   │   │   │   ├── companies.ts
│   │   │   │   ├── jobs.ts
│   │   │   │   ├── resumes.ts
│   │   │   │   ├── search.ts
│   │   │   │   └── matching.ts
│   │   │   ├── hooks/
│   │   │   │   ├── use-auth.ts
│   │   │   │   ├── use-candidate.ts
│   │   │   │   ├── use-jobs.ts
│   │   │   │   └── use-search.ts
│   │   │   ├── stores/
│   │   │   │   ├── auth-store.ts
│   │   │   │   ├── candidate-store.ts
│   │   │   │   └── search-store.ts
│   │   │   ├── utils/
│   │   │   │   ├── format.ts
│   │   │   │   ├── validation.ts
│   │   │   │   └── constants.ts
│   │   │   └── types/
│   │   │       ├── candidate.ts
│   │   │       ├── job.ts
│   │   │       ├── company.ts
│   │   │       ├── analysis.ts
│   │   │       └── common.ts
│   │   └── styles/
│   │       └── globals.css
│   ├── public/
│   ├── next.config.ts
│   ├── tailwind.config.ts
│   ├── tsconfig.json
│   ├── package.json
│   ├── Dockerfile
│   └── .env.example
├── docker/
│   ├── nginx/
│   │   └── nginx.conf
│   └── celery/
│       └── Dockerfile
├── docker-compose.yml
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── deploy.yml
├── docs/
│   ├── architecture.md
│   ├── database.md
│   ├── api.md
│   ├── ai-pipeline.md
│   ├── scoring.md
│   ├── prompts.md
│   ├── roadmap.md
│   └── ui.md
├── CLAUDE.md
├── README.md
├── .gitignore
└── .env.example
```

## Responsibilities

### Backend Modules

| Directory | Responsibility |
|-----------|---------------|
| `app/core/` | Configuration, database connections, external service clients, auth |
| `app/models/` | SQLAlchemy ORM models — one file per domain entity |
| `app/schemas/` | Pydantic request/response schemas — validation at API boundary |
| `app/repositories/` | Data access layer — all SQL queries live here (repository pattern) |
| `app/services/` | Business logic — orchestrates repositories and AI |
| `app/ai/client.py` | Gemini API wrapper with caching, retries, structured output |
| `app/ai/prompts/` | Prompt templates for each analyzer — isolated for iteration |
| `app/ai/analyzers/` | AI analysis services — one per evidence type |
| `app/ai/scoring/` | Cross-source scoring, evidence confidence, consistency checks |
| `app/ai/matching/` | Hybrid search, vector search, keyword search, reranker |
| `app/ai/generators/` | Summary, interview questions, skill gap, learning roadmap |
| `app/routers/` | FastAPI route handlers — thin, delegate to services |
| `app/tasks/` | Celery async tasks — background AI processing |
| `app/middleware/` | CORS, rate limiting, request IDs, error handling |

### Frontend Modules

| Directory | Responsibility |
|-----------|---------------|
| `src/app/` | Next.js app router pages and layouts |
| `src/components/ui/` | shadcn/ui primitives |
| `src/components/candidate/` | Candidate-specific components |
| `src/components/recruiter/` | Recruiter-specific components |
| `src/components/shared/` | Reusable components |
| `src/lib/api/` | API client and service-specific API functions |
| `src/lib/hooks/` | React hooks for data fetching and state |
| `src/lib/stores/` | Zustand state stores |
| `src/lib/types/` | TypeScript type definitions |
| `src/lib/utils/` | Formatting, validation, constants |

## Design Principles

- Feature-based module organization
- Clean Architecture (entities → use cases → interfaces → frameworks)
- Repository pattern for data access
- Dependency injection via FastAPI `Depends()`
- No circular imports
- Every AI call cached by input hash
- Structured JSON from every AI component
- No raw AI output stored — always parsed into typed models
