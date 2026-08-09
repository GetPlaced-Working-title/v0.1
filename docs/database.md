# Database Design

> PostgreSQL schema, ER diagram, relationships, and indexes.

## ER Diagram

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   users      │────▶│  candidates  │────▶│   resumes   │
│              │     │              │     │              │
│ id           │     │ id           │     │ id           │
│ clerk_id     │     │ user_id (FK) │     │ candidate_id │
│ email        │     │ name         │     │ file_url     │
│ role         │     │ headline     │     │ raw_text     │
│ created_at   │     │ location     │     │ analysis     │
│ updated_at   │     │ summary      │     │ scores       │
└─────────────┘     │ evidence_    │     │ status       │
       │            │  confidence  │     └─────────────┘
       │            │ profile_     │
       │            │  complete    │     ┌─────────────────┐
       │            └──────────────┘────▶│ github_profiles  │
       │                   │             │                  │
       │                   │             │ id               │
       │                   │             │ candidate_id     │
       ▼                   │             │ username         │
┌─────────────┐            │             │ analysis         │
│  companies   │            │             │ scores           │
│              │            │             └─────────────────┘
│ id           │            │
│ user_id (FK) │            │             ┌─────────────────┐
│ name         │            ├────────────▶│   portfolios     │
│ domain       │            │             │                  │
│ size         │            │             │ id               │
│ industry     │            │             │ candidate_id     │
└──────┬───────┘            │             │ url              │
       │                    │             │ analysis         │
       ▼                    │             │ scores           │
┌─────────────┐            │             └─────────────────┘
│    jobs      │            │
│              │            │             ┌──────────────────┐
│ id           │            ├────────────▶│ linkedin_exports  │
│ company_id   │            │             └──────────────────┘
│ title        │            │
│ description  │            │             ┌──────────────────┐
│ requirements │            ├────────────▶│    projects       │
│ embedding_id │            │             └──────────────────┘
│ status       │            │
└──────┬───────┘            │             ┌──────────────────┐
       │                    ├────────────▶│  certificates     │
       │                    │             └──────────────────┘
       ▼                    │
┌──────────────┐            │             ┌──────────────────┐
│ job_matches   │            ├────────────▶│     videos        │
│              │            │             └──────────────────┘
│ id           │            │
│ job_id       │            │             ┌──────────────────┐
│ candidate_id │            ├────────────▶│ recommendations   │
│ vector_score │            │             └──────────────────┘
│ rerank_score │            │
│ final_score  │            │             ┌──────────────────┐
│ status       │            ├────────────▶│  work_history     │
└──────────────┘            │             └──────────────────┘
                            │
                            │             ┌──────────────────┐
                            └────────────▶│     skills        │
                                          │                  │
                                          │ id               │
                                          │ candidate_id     │
                                          │ name             │
                                          │ confidence       │
                                          │ evidence_sources │
                                          │ verified         │
                                          └──────────────────┘
```

## Schema

### Core Tables

```sql
-- Base: all tables include these via mixin
-- id: UUID PRIMARY KEY DEFAULT gen_random_uuid()
-- created_at: TIMESTAMPTZ DEFAULT now()
-- updated_at: TIMESTAMPTZ DEFAULT now()
-- deleted_at: TIMESTAMPTZ NULL  (soft delete)

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    clerk_id VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'candidate',  -- candidate, recruiter, admin
    is_active BOOLEAN DEFAULT true,
    last_login_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now(),
    deleted_at TIMESTAMPTZ
);

CREATE TABLE companies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    name VARCHAR(255) NOT NULL,
    domain VARCHAR(255),
    website VARCHAR(500),
    industry VARCHAR(255),
    size VARCHAR(50),           -- startup, small, medium, large, enterprise
    description TEXT,
    logo_url VARCHAR(500),
    location VARCHAR(255),
    is_verified BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now(),
    deleted_at TIMESTAMPTZ
);

CREATE TABLE candidates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID UNIQUE NOT NULL REFERENCES users(id),
    name VARCHAR(255) NOT NULL,
    headline VARCHAR(500),
    location VARCHAR(255),
    phone VARCHAR(50),
    bio TEXT,
    years_of_experience DECIMAL(4,1),
    current_role VARCHAR(255),
    current_company VARCHAR(255),
    preferred_roles TEXT[],
    preferred_locations TEXT[],
    open_to_remote BOOLEAN DEFAULT true,
    salary_expectation_min INTEGER,
    salary_expectation_max INTEGER,
    salary_currency VARCHAR(10) DEFAULT 'USD',
    availability VARCHAR(50),       -- immediate, 2_weeks, 1_month, 3_months
    profile_completeness INTEGER DEFAULT 0,
    evidence_confidence VARCHAR(50) DEFAULT 'none', -- none, low, medium, high, very_high
    profile_summary JSONB,          -- AI-generated summary
    overall_scores JSONB,           -- Aggregated scores across all analyses
    profile_embedding_id VARCHAR(255), -- Qdrant point ID
    last_analyzed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now(),
    deleted_at TIMESTAMPTZ
);

CREATE TABLE jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID NOT NULL REFERENCES companies(id),
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    requirements JSONB,             -- structured requirements
    responsibilities TEXT[],
    required_skills TEXT[],
    preferred_skills TEXT[],
    experience_min INTEGER,
    experience_max INTEGER,
    education_level VARCHAR(100),
    employment_type VARCHAR(50),    -- full_time, part_time, contract, internship
    work_mode VARCHAR(50),          -- remote, hybrid, onsite
    location VARCHAR(255),
    salary_min INTEGER,
    salary_max INTEGER,
    salary_currency VARCHAR(10) DEFAULT 'USD',
    benefits TEXT[],
    status VARCHAR(50) DEFAULT 'draft', -- draft, active, paused, closed
    embedding_id VARCHAR(255),      -- Qdrant point ID
    applications_count INTEGER DEFAULT 0,
    matches_count INTEGER DEFAULT 0,
    expires_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now(),
    deleted_at TIMESTAMPTZ
);

-- Evidence Tables (one per evidence type)

CREATE TABLE resumes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    candidate_id UUID NOT NULL REFERENCES candidates(id),
    file_url VARCHAR(500) NOT NULL,
    file_name VARCHAR(255),
    file_size INTEGER,
    file_type VARCHAR(50),
    raw_text TEXT,                   -- extracted text
    basic_info JSONB,               -- name, contact, location, links
    experience JSONB,               -- parsed work experience
    education JSONB,                -- parsed education
    skills_extracted JSONB,         -- raw skill extraction
    projects_extracted JSONB,       -- projects found in resume
    certifications_extracted JSONB, -- certs found in resume
    achievements JSONB,             -- parsed achievements
    languages JSONB,                -- languages spoken
    publications JSONB,
    awards JSONB,
    analysis JSONB,                 -- full AI analysis result
    scores JSONB,                   -- experience_quality, achievement_quality, etc.
    resume_quality JSONB,           -- grammar, formatting, readability, etc.
    consistency_flags JSONB,        -- flags for cross-source verification
    missing_info JSONB,             -- identified gaps
    ats_compatibility JSONB,        -- ATS optimization score
    processing_status VARCHAR(50) DEFAULT 'pending',
    processing_error TEXT,
    is_primary BOOLEAN DEFAULT false,
    version INTEGER DEFAULT 1,
    analyzed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now(),
    deleted_at TIMESTAMPTZ
);

CREATE TABLE github_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    candidate_id UUID NOT NULL REFERENCES candidates(id),
    username VARCHAR(255) NOT NULL,
    profile_url VARCHAR(500),
    account_age_days INTEGER,
    public_repos INTEGER,
    followers INTEGER,
    following INTEGER,
    total_stars INTEGER,
    total_forks INTEGER,
    contribution_count INTEGER,
    primary_languages JSONB,        -- {language: percentage}
    repositories JSONB,             -- analyzed repos
    analysis JSONB,                 -- full AI analysis
    scores JSONB,                   -- technical_depth, code_quality, etc.
    skill_verification JSONB,       -- skills verified against code
    ai_code_detection JSONB,        -- estimated AI-generated code ratio
    processing_status VARCHAR(50) DEFAULT 'pending',
    processing_error TEXT,
    last_fetched_at TIMESTAMPTZ,
    analyzed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now(),
    deleted_at TIMESTAMPTZ
);

CREATE TABLE portfolios (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    candidate_id UUID NOT NULL REFERENCES candidates(id),
    url VARCHAR(500) NOT NULL,
    title VARCHAR(255),
    portfolio_type VARCHAR(50),     -- personal_website, behance, dribbble, etc.
    projects_found JSONB,           -- projects discovered on portfolio
    analysis JSONB,                 -- full AI analysis
    scores JSONB,                   -- design_quality, project_quality, etc.
    screenshots JSONB,              -- captured screenshots
    processing_status VARCHAR(50) DEFAULT 'pending',
    processing_error TEXT,
    last_crawled_at TIMESTAMPTZ,
    analyzed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now(),
    deleted_at TIMESTAMPTZ
);

CREATE TABLE linkedin_exports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    candidate_id UUID NOT NULL REFERENCES candidates(id),
    file_url VARCHAR(500),
    profile_url VARCHAR(500),
    headline VARCHAR(500),
    about TEXT,
    experience JSONB,
    education JSONB,
    certifications JSONB,
    skills JSONB,
    recommendations_received JSONB,
    endorsements JSONB,
    activity JSONB,
    analysis JSONB,
    scores JSONB,
    consistency_flags JSONB,
    processing_status VARCHAR(50) DEFAULT 'pending',
    processing_error TEXT,
    analyzed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now(),
    deleted_at TIMESTAMPTZ
);

CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    candidate_id UUID NOT NULL REFERENCES candidates(id),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    role VARCHAR(255),
    technologies TEXT[],
    url VARCHAR(500),
    github_url VARCHAR(500),
    live_url VARCHAR(500),
    start_date DATE,
    end_date DATE,
    is_ongoing BOOLEAN DEFAULT false,
    scope VARCHAR(50),              -- individual, team, startup, enterprise
    analysis JSONB,
    scores JSONB,
    source VARCHAR(50),             -- manual, resume, github, portfolio
    processing_status VARCHAR(50) DEFAULT 'pending',
    processing_error TEXT,
    analyzed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now(),
    deleted_at TIMESTAMPTZ
);

CREATE TABLE certificates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    candidate_id UUID NOT NULL REFERENCES candidates(id),
    name VARCHAR(255) NOT NULL,
    issuer VARCHAR(255),
    issue_date DATE,
    expiry_date DATE,
    credential_id VARCHAR(255),
    credential_url VARCHAR(500),
    file_url VARCHAR(500),
    difficulty_level VARCHAR(50),   -- beginner, intermediate, advanced, expert
    assessment_type VARCHAR(50),    -- exam, project, practical, attendance
    learning_hours DECIMAL(6,1),
    skills_covered TEXT[],
    analysis JSONB,
    scores JSONB,
    is_verified BOOLEAN DEFAULT false,
    verification_method VARCHAR(50),
    source VARCHAR(50),             -- manual, resume, linkedin
    processing_status VARCHAR(50) DEFAULT 'pending',
    processing_error TEXT,
    analyzed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now(),
    deleted_at TIMESTAMPTZ
);

CREATE TABLE videos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    candidate_id UUID NOT NULL REFERENCES candidates(id),
    title VARCHAR(255),
    description TEXT,
    file_url VARCHAR(500) NOT NULL,
    duration_seconds INTEGER,
    file_size BIGINT,
    thumbnail_url VARCHAR(500),
    transcript TEXT,
    analysis JSONB,
    scores JSONB,                   -- communication, confidence, etc.
    processing_status VARCHAR(50) DEFAULT 'pending',
    processing_error TEXT,
    analyzed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now(),
    deleted_at TIMESTAMPTZ
);

CREATE TABLE recommendations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    candidate_id UUID NOT NULL REFERENCES candidates(id),
    recommender_name VARCHAR(255),
    recommender_title VARCHAR(255),
    recommender_company VARCHAR(255),
    relationship VARCHAR(100),      -- manager, colleague, client, professor
    content TEXT,
    file_url VARCHAR(500),
    analysis JSONB,
    scores JSONB,
    source VARCHAR(50),             -- manual, linkedin
    processing_status VARCHAR(50) DEFAULT 'pending',
    processing_error TEXT,
    analyzed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now(),
    deleted_at TIMESTAMPTZ
);

CREATE TABLE work_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    candidate_id UUID NOT NULL REFERENCES candidates(id),
    company VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    location VARCHAR(255),
    start_date DATE,
    end_date DATE,
    is_current BOOLEAN DEFAULT false,
    employment_type VARCHAR(50),    -- full_time, part_time, contract, internship, freelance
    description TEXT,
    responsibilities TEXT[],
    achievements TEXT[],
    technologies TEXT[],
    analysis JSONB,
    scores JSONB,
    source VARCHAR(50),             -- manual, resume, linkedin
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now(),
    deleted_at TIMESTAMPTZ
);

-- Skills tracking with evidence

CREATE TABLE skills (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    candidate_id UUID NOT NULL REFERENCES candidates(id),
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100),          -- programming, framework, database, cloud, tool, soft_skill
    confidence VARCHAR(50) NOT NULL DEFAULT 'resume_mention',
    -- resume_mention, github_verified, portfolio_verified, assessment_verified, production_verified
    evidence_sources JSONB,         -- [{source: "resume", detail: "listed"}, {source: "github", detail: "50 commits"}]
    years_of_experience DECIMAL(4,1),
    last_used_date DATE,
    proficiency_level VARCHAR(50),  -- beginner, intermediate, advanced, expert
    verified BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now(),
    UNIQUE(candidate_id, name)
);

-- Matching and search

CREATE TABLE job_matches (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    job_id UUID NOT NULL REFERENCES jobs(id),
    candidate_id UUID NOT NULL REFERENCES candidates(id),
    vector_score DECIMAL(5,4),      -- raw cosine similarity
    keyword_score DECIMAL(5,4),     -- Meilisearch relevance
    hybrid_score DECIMAL(5,4),      -- merged score
    rerank_score DECIMAL(5,4),      -- LLM reranker score
    final_score DECIMAL(5,4),       -- final composite score
    rank INTEGER,
    match_details JSONB,            -- detailed match breakdown
    strengths JSONB,                -- why this candidate fits
    gaps JSONB,                     -- where candidate falls short
    interview_questions JSONB,      -- AI-generated questions
    status VARCHAR(50) DEFAULT 'matched', -- matched, shortlisted, contacted, rejected
    recruiter_notes TEXT,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now(),
    UNIQUE(job_id, candidate_id)
);

-- AI processing tracking

CREATE TABLE ai_analysis_cache (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    input_hash VARCHAR(64) NOT NULL UNIQUE,    -- SHA256 of input
    analyzer_type VARCHAR(100) NOT NULL,
    model_used VARCHAR(100),
    input_tokens INTEGER,
    output_tokens INTEGER,
    result JSONB NOT NULL,
    cost_usd DECIMAL(10,6),
    created_at TIMESTAMPTZ DEFAULT now(),
    expires_at TIMESTAMPTZ
);

-- Notifications

CREATE TABLE notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    type VARCHAR(100) NOT NULL,
    title VARCHAR(255) NOT NULL,
    message TEXT,
    data JSONB,
    read BOOLEAN DEFAULT false,
    read_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- Audit logs

CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(100),
    entity_id UUID,
    old_data JSONB,
    new_data JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);
```

## Indexes

```sql
-- Users
CREATE INDEX idx_users_clerk_id ON users(clerk_id);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);

-- Companies
CREATE INDEX idx_companies_user_id ON companies(user_id);
CREATE INDEX idx_companies_industry ON companies(industry);

-- Candidates
CREATE INDEX idx_candidates_user_id ON candidates(user_id);
CREATE INDEX idx_candidates_location ON candidates(location);
CREATE INDEX idx_candidates_evidence_confidence ON candidates(evidence_confidence);
CREATE INDEX idx_candidates_years_exp ON candidates(years_of_experience);

-- Jobs
CREATE INDEX idx_jobs_company_id ON jobs(company_id);
CREATE INDEX idx_jobs_status ON jobs(status);
CREATE INDEX idx_jobs_employment_type ON jobs(employment_type);
CREATE INDEX idx_jobs_work_mode ON jobs(work_mode);

-- Resumes
CREATE INDEX idx_resumes_candidate_id ON resumes(candidate_id);
CREATE INDEX idx_resumes_status ON resumes(processing_status);

-- GitHub profiles
CREATE INDEX idx_github_candidate_id ON github_profiles(candidate_id);
CREATE INDEX idx_github_username ON github_profiles(username);

-- Portfolios
CREATE INDEX idx_portfolios_candidate_id ON portfolios(candidate_id);

-- LinkedIn
CREATE INDEX idx_linkedin_candidate_id ON linkedin_exports(candidate_id);

-- Projects
CREATE INDEX idx_projects_candidate_id ON projects(candidate_id);

-- Certificates
CREATE INDEX idx_certificates_candidate_id ON certificates(candidate_id);

-- Videos
CREATE INDEX idx_videos_candidate_id ON videos(candidate_id);

-- Recommendations
CREATE INDEX idx_recommendations_candidate_id ON recommendations(candidate_id);

-- Work history
CREATE INDEX idx_work_history_candidate_id ON work_history(candidate_id);

-- Skills
CREATE INDEX idx_skills_candidate_id ON skills(candidate_id);
CREATE INDEX idx_skills_name ON skills(name);
CREATE INDEX idx_skills_confidence ON skills(confidence);
CREATE INDEX idx_skills_candidate_name ON skills(candidate_id, name);

-- Job matches
CREATE INDEX idx_matches_job_id ON job_matches(job_id);
CREATE INDEX idx_matches_candidate_id ON job_matches(candidate_id);
CREATE INDEX idx_matches_final_score ON job_matches(final_score DESC);
CREATE INDEX idx_matches_status ON job_matches(status);

-- AI cache
CREATE INDEX idx_ai_cache_hash ON ai_analysis_cache(input_hash);
CREATE INDEX idx_ai_cache_type ON ai_analysis_cache(analyzer_type);

-- Notifications
CREATE INDEX idx_notifications_user_id ON notifications(user_id);
CREATE INDEX idx_notifications_read ON notifications(user_id, read);

-- Audit
CREATE INDEX idx_audit_user_id ON audit_logs(user_id);
CREATE INDEX idx_audit_entity ON audit_logs(entity_type, entity_id);
CREATE INDEX idx_audit_created ON audit_logs(created_at);

-- Partial indexes for active records (soft deletes)
CREATE INDEX idx_users_active ON users(id) WHERE deleted_at IS NULL;
CREATE INDEX idx_candidates_active ON candidates(id) WHERE deleted_at IS NULL;
CREATE INDEX idx_jobs_active ON jobs(id) WHERE deleted_at IS NULL AND status = 'active';
```
