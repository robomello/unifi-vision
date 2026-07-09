---
name: SafePlate
description: Restaurant allergen safety platform MVP -- Next.js 15, Prisma, PostgreSQL, Leaflet, 78+ allergens, dual ratings, i18n
type: project
---

## SafePlate -- Restaurant Discovery for Food Allergies

- **Location**: `/home/mello/commander/projects/safeplate/`
- **Port**: 3030 (mapped 127.0.0.1:3030:3000)
- **Subdomain**: safeplate.synai.ai (needs CF Tunnel route -- container deployed but no public route yet)
- **Container**: on n8n-net, shares n8n-postgres (database: `safeplate`)
- **Stack**: Next.js 15 App Router + Prisma 6 + PostgreSQL + Tailwind CSS v4 + Leaflet

**Target market**: 33M Americans with food allergies, 3.3M with celiac disease, 21M gluten avoiders.

**Core features (MVP)**:
1. Dual rating system (safety + food quality)
2. Cross-contamination details (dedicated fryer, separate prep, etc.)
3. Allergen filtering (78+ allergens, FDA Top 9 flagged)
4. "Suggest a Restaurant" form
5. Map/list view toggle (Leaflet + OSM, free)
6. Reviewer credibility indicators
7. i18n: 7 languages (EN, ES, FR, PT, ZH, KO, JA) via lightweight React Context

**Auth**: iron-session (cookie-based, same pattern as Mello Garden).
**Schema**: 11 Prisma models (users, restaurants, reviews, allergens, claims, suggestions).

### Timeline
- 2026-04-04: Planned, built, i18n added
- 2026-04-05: Deployed to Docker (container `safeplate`, running healthy)

### What's deferred
- External data seeding (OSM, Foursquare, Google Places, chain PDFs)
- SMS verification for claims (form-only placeholder)
- Mobile native app, payment/subscription
- Rate limiting

**Why:** New business idea targeting underserved market. Strategy docs exist from Claude.ai sessions (community growth playbook + feasibility study).

**How to apply:** When working on SafePlate, reference the plan at `/home/mello/.claude/plans/hashed-dreaming-quiche-agent-*.md`. Build/deploy: `cd /home/mello/commander/projects/safeplate && docker compose build --no-cache && docker compose up -d`.
