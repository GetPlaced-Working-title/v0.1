# Roadmap

> Development milestones for AI Talent Router.

## Milestone 1: Foundation (Current)
- [x] Project architecture and documentation
- [x] Database schema and models
- [x] Core infrastructure (config, database, Redis, Qdrant, Meilisearch, storage)
- [x] AI client and caching layer
- [x] All prompt templates
- [x] Backend API (schemas, repositories, services, routers)
- [x] Celery task definitions
- [x] Alembic migration setup
- [x] Docker Compose for all services
- [x] Frontend scaffolding with all pages
- [x] CI/CD pipeline

## Milestone 2: Core Features
- [ ] Resume upload + text extraction (PDF parsing)
- [ ] Resume AI analysis
- [ ] GitHub account connection + analysis
- [ ] Portfolio URL analysis
- [ ] Certificate upload + verification
- [ ] Profile aggregation and scoring
- [ ] Candidate dashboard with scores

## Milestone 3: Matching
- [ ] Embedding generation for candidates and jobs
- [ ] Vector search in Qdrant
- [ ] Meilisearch keyword indexing
- [ ] Hybrid search merging
- [ ] AI reranker for job-candidate matching
- [ ] Recruiter match dashboard

## Milestone 4: Video Analysis
- [ ] Video upload to R2
- [ ] Gemini Video analysis
- [ ] Communication and confidence scoring
- [ ] Video gallery in candidate profile

## Milestone 5: Production
- [ ] Clerk authentication integration
- [ ] Role-based access control
- [ ] Notification system
- [ ] Admin analytics dashboard
- [ ] Rate limiting and abuse prevention
- [ ] Production deployment on Coolify
- [ ] Monitoring and alerting
