---
name: YouTube Infrastructure
description: YouTube uploader (port 8055), 5 registered accounts (PulpArena, Evolution, Khooni, RobertoMello79, SleepAid), 3 agents (analytics, uploader, SEO), hunter, channel-factory. Bible pipeline planned but blocked.
type: reference
---

## YouTube Infrastructure (Uploader, Agents, Tools)

### YouTube Uploader Service
**Location:** /home/mello/commander/projects/youtube-uploader/
**Container:** youtube-uploader (running, port 8055)
**Architecture:** FastAPI with OAuth2 flow for YouTube Data API v3
**Capabilities:** OAuth auth flow (/auth/start -> /auth/callback), resumable video upload (/upload), token auto-refresh

### Registered YouTube Accounts:
| Account | Env Prefix | Purpose |
|---------|-----------|---------|
| PULPARENA | YOUTUBE_PULPARENA_ | Content channel |
| EVOLUTION | YOUTUBE_EVOLUTION_ | Content channel |
| KHOONI | YOUTUBE_KHOONI_ | Content channel (ID: UCAKpVAcuZ2s4h8XgMyUrluw) |
| ROBERTOMELLO79 | YOUTUBE_ROBERTOMELLO79_ | Personal channel |
| SLEEPAID_AI | YOUTUBE_SLEEPAID_AI_ | Sleep AI channel (placeholder token) |

### YouTube Agents (3 Claude subagents, all Haiku):
1. **youtube-analytics-agent** — Fetch channel/video stats via YouTube Data API v3 (PulpArena, Evolution, Khooni)
2. **youtube-uploader-agent** — Upload videos via resumable upload with OAuth
3. **youtube-seo-agent** — Generate SEO-optimized titles (<70 chars), descriptions (2000+ chars), tags (15-20)

### Channel management scripts:
- /home/mello/commander/projects/youtube-add-channel.py — Browser-based OAuth for adding channels
- /home/mello/commander/projects/youtube-add-channel-manual.py — Headless/manual OAuth
- /home/mello/commander/projects/youtube-uploader/verify_channel.py — Verify credential-to-channel mapping

### Other YouTube tools:
- commander/tools/scrape.py — youtube_scrape_channel, youtube_scrape_videos, youtube_video_details, youtube_search, youtube_comments (ScrapeCreators API)
- claude-seo/scripts/youtube_search.py — YouTube Data API v3 for SEO (notes YouTube mentions have 0.737 AI visibility correlation)
- commander/tools/god_research/ — Multi-source research including YouTube pain-point queries

### Bible YouTube Pipeline (PLANNED, NOT BUILT):
**Plan:** /home/mello/commander/projects/bible-youtube-pipeline-PLAN.md
**Status:** DRAFT (2026-04-15), BLOCKED on ElevenLabs API key + YouTube BIBLE channel credentials
**Format:** 'Every X in the Bible' (based on Deep Made Simple analysis showing 133K avg views)
**Target:** 1 video/day, 4-6 min duration
**6-phase pipeline:** Topic Research -> Script -> Visual -> Audio -> Assembly -> Upload

Why: YouTube infrastructure spans 5 accounts, 3 agents, uploader service, and multiple tools. Not comprehensively documented in memory.

How to apply: For uploads use youtube-uploader-agent or POST to youtube-uploader:8055. For stats use youtube-analytics-agent. For SEO use youtube-seo-agent. Channel creds in ~/.env.
