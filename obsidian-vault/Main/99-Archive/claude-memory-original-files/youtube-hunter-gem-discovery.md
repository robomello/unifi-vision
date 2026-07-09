---
name: YouTube Hunter (Gem Discovery)
description: Viral video finder at /home/mello/commander/projects/youtube-hunter/. LangGraph workflow, gem_score=views/subs, saves to NocoDB table m11oy6r9nw13g0a. Container: youtube-hunter.
type: project
---

## YouTube Hunter (Viral Gem Discovery)

**Location:** /home/mello/commander/projects/youtube-hunter/
**Container:** youtube-hunter (running, healthy)
**Architecture:** LangGraph workflow with 5 nodes: search -> fetch_channels -> fetch_videos -> filter -> save
**Status:** Active

### What It Does
Finds viral 'gems' — videos from small channels with disproportionate views. Searches a niche, fetches video + channel stats, filters by views/subscribers ratio.

### Configuration defaults:
- Minimum views: 500,000
- Maximum channel subscribers: 10,000
- Maximum results: 50
- gem_score = views / subs

### NocoDB Integration:
- Table ID: m11oy6r9nw13g0a (youtube_gems table)
- NocoDB URL: https://nocodb.synai.ai
- Fields: niche, channel_name, video_title, video_url, views, subs, channel_videos, score, video_type, duration, posted_at, found_at

### Key files:
- youtube_hunter/models.py — Pydantic models (HunterConfig, VideoStats, ChannelStats, HunterGem, HuntResult)
- youtube_hunter/client.py — Async YouTube Data API v3 client with OAuth
- youtube_hunter/nocodb.py — NocoDB client for saving gems
- youtube_hunter/graph/ — LangGraph workflow

Why: youtube-hunter is the viral video discovery tool for content strategy. Not documented in memory.

How to apply: When looking for viral video ideas in a niche, use youtube-hunter. Results saved to NocoDB youtube_gems table.
