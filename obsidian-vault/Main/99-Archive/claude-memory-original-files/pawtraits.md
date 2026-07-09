---
name: Pawtraits
description: AI dog portrait service at pawtraits.synai.ai -- Next.js, Stripe, CF edge caching, flashlight gallery effect
type: project
---

## Pawtraits -- AI Pet Portrait Service

- **Location**: `/home/mello/commander/projects/pawtraits/`
- **Port**: 3101
- **Subdomain**: pawtraits.synai.ai (CF Tunnel active)
- **Stack**: Next.js (standalone build), Docker
- **Deploy**: `docker compose --env-file /home/mello/.env -f /home/mello/commander/projects/pawtraits/docker-compose.pawtraits.yml build pawtraits-web --no-cache && docker stop pawtraits-web && docker rm pawtraits-web && docker compose --env-file /home/mello/.env -f /home/mello/commander/projects/pawtraits/docker-compose.pawtraits.yml up -d pawtraits-web`

**Features**:
- Landing page with 8 dog style cards + flashlight background reveal effect
- Code splitting, WebP images, ISR pre-rendering
- CF edge caching (CDN-Cache-Control headers, Cache Rule for `/` path, 1h TTL)

### Recent work (2026-04-04)
- Fixed slow loading: added CF Cache Rule so landing page gets edge-cached (MISS->HIT)
- Flashlight effect reworked: images always visible, flashlight reveals background only (grid pattern + gradient orbs in gaps between cards)

**How to apply:** Uses a custom docker-compose file (`docker-compose.pawtraits.yml`) with `--env-file /home/mello/.env`. Not in the main docker-compose.yml.
