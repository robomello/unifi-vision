# Handoff: YouTube Video Analyzer Page

**Date**: 2026-03-14 16:13:24 (UTC-6)
**Project**: Home Server (mello)
**Branch**: N/A (not a git repo)
**Session Summary**: Built a YouTube video analysis pipeline that extracts transcripts + frames from videos, produces comprehensive markdown analyses, and serves them on a web page at https://yt.synai.ai. Analyzed 5 videos total (4 from user links + 1 from a background agent).

## Completed This Session
- Extracted and analyzed 5 YouTube videos using the youtube-analyzer skill (transcript + frame-by-frame visual analysis)
- Video 1 (Mark Kashef - "Most Underrated Feature of Claude Code") analyzed manually with full frame reads (uncommitted)
- Videos 2-5 analyzed via parallel background agents (uncommitted)
- Created web page at `/data/sites/yt-analyses/index.html` with sidebar navigation, markdown rendering via marked.js, dark theme
- Created `manifest.json` for dynamic video listing
- Spun up `yt-analyses` Docker container (nginx:alpine) on port 3020 serving `/data/sites/yt-analyses/`
- Connected container to `n8n-net` Docker network for cloudflared access
- Added Cloudflare Tunnel route (`yt.synai.ai` -> `yt-analyses:80`) via API
- Created DNS CNAME record (`yt.synai.ai` -> tunnel) via Cloudflare API
- Site is live at https://yt.synai.ai

## Known Issues
- Server's local DNS resolver had negative cache for `yt.synai.ai` after initial failed lookups. Resolved externally (Google/Cloudflare DNS) but server-side curl fails without `--resolve` flag. `systemctl restart systemd-resolved` may fix, or just wait for cache expiry. (severity: low)
- The `yt-analyses` container is not in `docker-compose.yml` -- it was started with `docker run`. Needs to be added to compose for persistence across server restarts. (severity: medium, file: `docker-compose.yml`)
- Ryan Hogue video view count in manifest is estimated (4500) since exact count wasn't captured. (severity: low, file: `/data/sites/yt-analyses/manifest.json`)

## Key Decisions Made
- **Decision**: Used nginx:alpine standalone container instead of adding to existing service
  **Reasoning**: Fastest path to serve static files. Could be folded into docker-compose later.
- **Decision**: Manifest-driven page architecture (manifest.json + markdown files)
  **Reasoning**: Easy to add new videos -- just drop a .md file and update manifest.json. No rebuild needed.
- **Decision**: Cloudflare Tunnel route added via API (not dashboard)
  **Reasoning**: User confirmed full Cloudflare API access. Used existing env vars from `~/.env`.

## Next Steps (Priority Order)
1. **Add `yt-analyses` to `docker-compose.yml`** -- container will be lost on server restart otherwise
2. **Automate video addition** -- could create a skill/command that takes a YouTube URL, runs the analyzer, copies output to `/data/sites/yt-analyses/`, and updates manifest.json automatically
3. **Improve the page** -- add search, video thumbnails, link back to original YouTube URL, sort options

## Files Actively Being Edited
- `/data/sites/yt-analyses/index.html` -- main web page, fully functional
- `/data/sites/yt-analyses/manifest.json` -- video listing, 5 entries
- `/data/sites/yt-analyses/*.md` -- 5 analysis markdown files
- `commander/projects/youtube-analyses/*.md` -- source copies of all analyses

## Context for Next Session
- Cloudflare Tunnel config was updated via PUT to `/accounts/{id}/cfd_tunnel/{tunnel_id}/configurations`. The full ingress list must be sent each time (it replaces, not appends). Current version: 54.
- Tunnel ID: `9f023bc5-0c1e-4fa7-8d6c-96d22d613966`
- DNS record ID for yt.synai.ai: `720d14bd766214c3f69fac1889e8566d`
- The `yt-analyses` container is on both `bridge` (default) and `n8n-net` networks
- Cloudflare API creds are in `/home/mello/.env` as `CLOUDFLARE_ACCOUNT_ID`, `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ZONE_ID`

## Videos Analyzed
1. Mark Kashef - "Most Underrated Feature of Claude Code" (11:07) -- @claude-code-guide sub-agent, 5 levels of usage
2. Simon Scrapes - "Build Self-Improving Claude Code Skills" (11:02) -- Karpathy-style autoresearch for Claude Code skills
3. Ryan Hogue - "Etsy Finally Has a Competitor - Faire POD" (7:26) -- Faire wholesale marketplace for POD sellers
4. Jake Van Clief - "Claude Code + Remotion" (22:30) -- Script-to-animated-video pipeline
5. Jack Roberts - "Perplexity Computer + Claude" (25:10) -- Perplexity's AI agent product review

## Git State
- Not a git repository
- No commits
- All changes are on disk only
