---
name: FB Reels Scraping via yt-dlp
description: FB reels require yt-dlp (DASH streaming, no direct src); Playwright collects IDs; yt-dlp downloads; use ?sk=reels_tab URL
type: reference
---

FB reels use DASH streaming — `<video src>` is always None even when logged in headless. Use `yt-dlp --cookies cookies/netscape.txt` (Netscape format, auto-generated from latest.json) to download. Scroll `?sk=reels_tab` (not `?sk=reels` or `?sk=videos`) with Playwright to collect reel IDs first. KnowBit result: 70 reels vs 10 with stale cookies. download_reels.py exists at /home/mello/commander/projects/facebook/download_reels.py.

**Why:** FB serves reels via DASH segments (~500KB chunks), not a single playable_url. yt-dlp handles FB DASH + authentication automatically.
**How to apply:** When asked to scrape reels, use download_reels.py. When extending to new pages, edit PROFILE_ID + SLUG at top of the script.
