# UI/UX Design Notes

> Frontend design system and page structure.

## Design System

- **Framework**: Next.js 15 App Router
- **Styling**: Tailwind CSS + shadcn/ui
- **State**: Zustand for client state, React Query for server state
- **Font**: Inter (Google Fonts)
- **Theme**: Light/dark via CSS custom properties

## Page Structure

### Public
- `/` — Landing page with hero, features, how-it-works
- `/sign-in` — Authentication
- `/sign-up` — Role selection (candidate/recruiter)

### Candidate Portal
- `/candidate/dashboard` — Overview with stats and quick actions
- `/candidate/profile` — Edit profile, connect sources, view scores
- `/candidate/resume` — Upload and view resumes
- `/candidate/projects` — Add and manage projects
- `/candidate/certificates` — Add certificates
- `/candidate/videos` — Upload skill demo videos
- `/candidate/settings` — Account settings

### Recruiter Portal
- `/recruiter/dashboard` — Overview with jobs, matches, quick actions
- `/recruiter/jobs` — Create and manage job postings
- `/recruiter/candidates` — Browse and search candidates
- `/recruiter/search` — Advanced candidate search
- `/recruiter/matches` — View AI matches for jobs
- `/recruiter/settings` — Company profile settings

### Admin Portal
- `/admin/dashboard` — Platform stats and system health
- `/admin/users` — User management
- `/admin/analytics` — AI usage and cost tracking

## Component Architecture

- `components/ui/` — shadcn/ui primitives (Button, Card, Input, Badge)
- `components/layout/` — Header, Sidebar
- `components/candidate/` — ProfileCard, SkillBadge, ScoreRadar, EvidenceIndicator, ResumeUpload, GitHubConnect
- `components/recruiter/` — CandidateCard, JobForm, MatchScore, SearchFilters
- `components/shared/` — Loading, ErrorBoundary, FileUpload, DataTable

## Key Interactions

1. **Evidence Upload**: Drag-and-drop file upload with progress
2. **GitHub Connect**: Username input with validation
3. **Job Creation**: Multi-field form with skill tags
4. **Candidate Search**: Filters + keyword + Meilisearch results
5. **Matching**: One-click match run, ranked results with score breakdown
