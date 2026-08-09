# AI Talent Router

An AI-powered hiring platform that understands candidates from evidence instead of keywords.

## Overview

AI Talent Router analyzes candidate artifacts — resumes, GitHub profiles, portfolios, videos, certificates, and more — to build rich, structured profiles. Recruiters don't browse resumes. They describe a role, and the system returns the best matches using vector search and AI reranking.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 15, TypeScript, Tailwind, shadcn/ui |
| Backend | FastAPI, SQLAlchemy, Pydantic, Alembic |
| Database | PostgreSQL |
| Cache | Redis |
| Vector DB | Qdrant |
| Search | Meilisearch |
| Storage | Cloudflare R2 |
| Queue | Celery |
| AI | Gemini Flash Lite, Gemini Video, Gemini Embeddings |
| Deploy | Docker, Coolify |

## Getting Started

### Prerequisites

- Docker & Docker Compose
- Node.js 20+
- Python 3.12+
- Gemini API key

### Quick Start

```bash
# Clone the repo
git clone <repo-url>
cd talent-ai

# Start all services
docker compose up -d

# Backend
cd backend
cp .env.example .env
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
cd frontend
cp .env.example .env.local
npm install
npm run dev
```

## Documentation

| Doc | Description |
|-----|-------------|
| [Architecture](docs/architecture.md) | Folder structure and module responsibilities |
| [Database](docs/database.md) | ER diagram, schema, indexes |
| [API](docs/api.md) | REST endpoints, request/response shapes |
| [AI Pipeline](docs/ai-pipeline.md) | Analysis pipeline and inference design |
| [Roadmap](docs/roadmap.md) | Milestones and delivery plan |
| [Prompts](docs/prompts.md) | AI prompt templates |
| [Scoring](docs/scoring.md) | Candidate scoring and ranking logic |
| [UI](docs/ui.md) | UI/UX design notes |

## License

MIT
