---
name: search-strategy
description: Where to look first when finding services/projects -- Docker first, then check multiple locations
type: feedback
---

When looking for a service or website, ALWAYS check `docker-compose.yml` and `docker ps` FIRST -- most things run in Docker.

Not all projects live in `/data/sites/` or `commander/projects/` -- some are top-level in `/home/mello/` (e.g., `mello-garden/`).

**Why:** Multiple times I searched the wrong directories and missed projects that were right there in Docker or in unexpected locations.

**How to apply:** For any "where is X?" question: `docker ps | grep X` first, then check docker-compose.yml, then `/home/mello/`, then `commander/projects/`, then `/data/sites/`.
