# Engineering Preferences

## Languages & Frameworks
- Frontend: Next.js 15 + TypeScript + Tailwind CSS + shadcn/ui. Confidence: 0.9
- Backend: FastAPI (Python) + SQLAlchemy + Pydantic. Prefers Python for backend because it provides the richest AI ecosystem without cross-language bridges. Confidence: 0.9
- Strict TypeScript on frontend, fully typed Python on backend. Confidence: 0.9

## Architecture
- Prefers clean architecture with repository pattern, modular/feature-based folder structure. Confidence: 0.9
- No duplicated logic. Every feature must be documented. Tests required and must pass without errors — test suites that fail or are skipped are not acceptable. Confidence: 0.9
- Environment variables for secrets — never hardcode. Confidence: 0.95

## Database & Search
- PostgreSQL for relational data. Confidence: 0.9
- Hybrid search combining keyword (Meilisearch) and semantic (Qdrant/vector) search, merged for better retrieval than either alone. Confidence: 0.85
- Redis for caching and as message broker (Celery). Confidence: 0.85

## Storage & Hosting
- Strong preference for Cloudflare R2 over S3 — specifically for zero egress charges. Confidence: 0.9
- Self-hosts databases and search services on VPS (Hetzner) rather than using managed cloud services. Confidence: 0.85
- Docker + Coolify for deployment. Confidence: 0.8

## AI Architecture
- Prefers lightweight/cost-optimized models (Gemini Flash Lite) for high-volume inference tasks. Confidence: 0.9
- AI inference only during profile creation/update — never during real-time search. Deterministic systems for retrieval and ranking. Confidence: 0.9
- Always cache AI results. Analyze once, store structured output, reuse. Confidence: 0.9
- Structured JSON output from all AI services — never store natural language when structured data works. Confidence: 0.9
- LLM reranker applied only to top N candidates from deterministic search, not the entire corpus. Confidence: 0.85
- Plans for local embedding migration (FastEmbed/BGE-small) if API costs grow. Confidence: 0.75

## Global / Remote-First Design
- Products intended for global audiences must include RTL/bidirectional text support from the start. Uses logical CSS properties (me-/ms-/ps-/pe-) instead of physical (mr-/ml-/pl-/pr-), `dir` attribute support, and safe-area padding. Treats this as part of a "remote policy." Confidence: 0.7

## State Management
- Zustand for frontend state. Confidence: 0.8
- React Hook Form + Zod for forms/validation. Confidence: 0.8
