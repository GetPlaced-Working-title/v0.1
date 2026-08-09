# Workflow Preferences

## Development Process
- Creates detailed roadmaps with 30-40 milestones and works through them sequentially. Completes, tests, documents, and reviews each milestone before proceeding. Confidence: 0.9
- Breaks implementation into ordered commands: (1) analyze/create folder architecture, (2) design database, (3) design APIs, (4) design AI pipeline, (5) build backend, (6) build frontend, (7) implement AI services, (8) Docker/deployment, (9) review and fix. Confidence: 0.9
- Uses sub-agents for parallel work, assigning different models to main vs. sub-agents. Confidence: 0.8

## AI Coding Tool Usage
- Uses `/model` command frequently to switch between models for different tasks. Confidence: 0.8
- Prefers persistent project context files (CLAUDE.md) over re-explaining architecture each session. Confidence: 0.9
- Uses `/compact` to manage context window, `/clear` for fresh sessions while retaining project context. Confidence: 0.8

## Documentation
- Expects comprehensive docs: architecture.md, database.md, ai-pipeline.md, api.md, roadmap.md, prompts.md, scoring.md, ui.md. Confidence: 0.85
- Every feature must be documented as a coding standard. Confidence: 0.85

## Review Process
- Dedicated review step at the end of each major phase: bugs, security issues, performance, architecture, duplicate code, memory leaks, race conditions. Confidence: 0.85
- Uses `/design` command (checkup, responsive, surface, recolor modes) as a structured UI/UX audit before considering frontend work complete. Design issues found in checkup are treated as blockers, not suggestions. Confidence: 0.7

## Execution Style
- Expects autonomous end-to-end task completion — explicitly instructs "don't stop until you complete it" and prefers using automation/loops features for efficiency rather than pausing for confirmation between steps. Confidence: 0.85
