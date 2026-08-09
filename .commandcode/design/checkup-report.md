# GetPlaced — Checkup

**Date:** 2026-08-06
**Mode:** `/design checkup`
**Surface:** Full frontend (Next.js 15 App Router, Tailwind, shadcn/ui)

## Composition Vital Sign

**Status: Healthy (10/10)**

The app follows Monitor/Operate compositions appropriately:
- Candidate dashboard: Monitor pattern — stats at top, quick actions below, recent activity panel
- Recruiter dashboard: Operate pattern — metrics row, actions, jobs list
- Job form: Configure pattern — grouped fields, clear submission
- Search pages: Explore pattern — filters, grid results
- Landing page: Decide pattern — hero with proof, CTA, feature cards

Composition matches the work. No forced card layouts where tables belong.

## Scoring

| # | Heuristic | Score | Status | Key Finding |
|---|-----------|-------|--------|-------------|
| 1 | Intentionality | 7/10 | Watch | Tailwind defaults throughout; no brand color differentiation, no authored visual identity beyond palette |
| 2 | Readability | 8/10 | Watch | Body text is readable, but Input/select/textarea all use `text-sm` (14px) — iOS Safari auto-zoom bug on mobile |
| 3 | Usability | 5/10 | Critical | Missing loading, empty, error states on 80% of pages; no keyboard navigation path tested; no screen-reader support |
| 4 | Responsiveness | 5/10 | Critical | No RTL support; mobile sidebar is fixed 256px (consumes full phone width); no safe-area padding; hardcoded `mr-`/`ml-` instead of logical properties |
| 5 | Speed | 10/10 | Healthy | Static site with client components; no image loading issues detected; React Query with reasonable stale time |
| 6 | Accessibility | 3/10 | Critical | No aria-labels on form controls; no skip links; color-only indicators (score colors, confidence badges); no reduced-motion handling; FileUpload id collision; selects lack focus rings |

**TOTAL: 38/60**

## Priority Issues

### P0: No RTL / direction support (Accessibility + Responsive)
Every layout component uses `mr-`/`ml-`/`pl-`/`pr-` instead of logical `me-`/`ms-`/`ps-`/`pe-`. The product cannot render Arabic, Hebrew, Farsi, or Urdu. Fix: swap all physical CSS properties to logical ones.

### P0: iOS Safari input zoom on all form controls (Readability + Responsive)
Every `Input`, `select`, `textarea` uses `text-sm` (14px or 0.875rem). Below 16px on screens < 640px, iOS Safari triggers automatic viewport zoom on focus. Fix: `text-base sm:text-sm` on all form controls.

### P0: Missing state coverage (Usability)
Pages show ideal state only. No loading spinners on data-dependent pages, no error boundaries wired in, no empty state teaching copy (just "no data"). Candidates and recruiters cannot complete core tasks without these.

### P1: Accessibility gaps (Accessibility)
- No aria-labels on form controls
- Color-only indicators (confidence badges, score colors) — no icons or patterns
- No reduced-motion media query handling
- FileUpload uses a fixed `id="file-upload"` — creates DOM conflicts with multiple uploaders

### P2: Visual identity (Intentionality)
The app uses Tailwind defaults without a distinct visual lane. Same gray tones as every other SaaS dashboard. No brand differentiation.

## Next Modes

- `/design responsive` — fix RTL + mobile sidebar + iOS input zoom
- `/design surface` — add loading/empty/error states across all pages
- `/design recolor` — tighten the color system with brand-specific hues
