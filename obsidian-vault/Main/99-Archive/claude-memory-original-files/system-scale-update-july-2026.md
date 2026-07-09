---
name: System Scale Update July 2026
description: Current infrastructure: 88 containers, 89 agents, 33 skills, 211 projects. New observability stack, media pipelines, and recent projects documented.
type: reference
---

## System Scale Update (2026-07-05)

Current infrastructure as of scan:
- **88 running Docker containers** (up from ~40 previously documented)
- **89 agents** in ~/.claude/agents/
- **33 skills** in ~/skills/
- **211 project directories** in ~/commander/projects/
- **13 rules files** in ~/.claude/rules/

### Notable New Containers (not in previous memory)

**Observability Stack:**
- claudicle-ui, claudicle-clickhouse, claudicle-otel (Claude usage tracking)
- prometheus, promtail, loki, cadvisor (system monitoring)

**Media/Video Pipelines:**
- videogen-factory, videogen-worker (video generation)
- avatar-pipeline (avatar video generation)
- media-server (media serving)

**Recent Projects:**
- ai-psychologist (active Jul 5)
- pxpipe-recall-bench (Jul 4, recall testing)
- unifi-vision (Jul 3, UniFi camera integration)
- youtube-analyses (Jul 5, YouTube analytics)
- tiktok-shop-dashboard (TikTok Shop UI)
- yt-analyses, youtube-hunter (YouTube tools)

**Infrastructure:**
- flaresolverr (Cloudflare bypass)
- n8n-db-cleaner (database maintenance)
- gasbuddy-scraper (fuel price scraping)
- printwalk, privacy-policy, roi-static (misc services)

Why: System has grown significantly. Memory referenced ~49 agents but we now have 89. Container count at 88 indicates substantial infrastructure expansion.

How to apply: When searching for capabilities, check the full container list (docker ps) not just remembered projects. Many new services exist that aren't in project memory yet.
