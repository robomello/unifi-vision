---
name: Skool reply pipeline: group discovery uses /self/groups not allGroups
description: skool-api get_my_groups must hit api2.skool.com/self/groups?limit=100; the page-embedded allGroups truncates at ~11 and silently drops real memberships
type: project
---

The skool-api scraper (`/home/mello/commander/projects/skool-api/app/scraper.py`) used to read groups from the etsydesignclub page's `pageProps.self.allGroups`. That field is **truncated to ~11 entries** by Skool, so memberships like `scrapes`, `ai-automation-society-plus`, `ai-art-sellers-collective`, and `creator-secrets-4381` were silently invisible to the pipeline (no posts pulled, no dashboard card).

The fix (2026-05-19): switch `get_my_groups()` to hit `https://api2.skool.com/self/groups?limit=100`, which returns the full membership list (15 entries for Roberto). The old allGroups path is kept as a fallback if that endpoint ever fails.

**Why:** Skool truncates the SSR session blob; the api2 endpoint is the authoritative source. Without `?limit=100` it also defaults to 10.

**How to apply:** If a Skool the user clearly belongs to is missing from the dashboard or feed sync, check `/self/groups?limit=100` first — don't trust the page-embedded `allGroups`. Also note the `SKOOL_EXTRA_GROUPS` env var on the `skool-api` service in `/home/mello/docker-compose.yml`: comma-separated slugs there are appended to the joined list, intended for read-only monitoring of Skools the user is not a member of.

Related: dashboard at `https://localhost:8092` (skool-reply container), API on 8091.
