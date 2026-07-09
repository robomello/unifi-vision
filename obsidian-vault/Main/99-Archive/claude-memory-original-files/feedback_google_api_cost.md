---
name: Google API Cost Control
description: Google Places API must be on-demand only, max 1 fetch per zone per day -- no automatic background refreshes
type: feedback
---

Google Places API calls MUST be strictly on-demand (user clicks "Search this area") and limited to max 1 fetch per zone per 24 hours. No automatic background refresh loops for paid sources.

**Why:** Roberto is cost-conscious about the Google Places API ($40/1K calls). The zone refresh loop was burning API budget on areas nobody was viewing. He explicitly asked for "on-demand, not more than 1 per day."

**How to apply:** When building features that query Google Places:
- Never pre-fetch or auto-refresh paid data sources
- Always check zone.lastFetchedAt and enforce 24h cooldown
- Free government APIs (FR, ES, AT, DE) can run on cron freely
- Only user-initiated actions should trigger paid API calls
