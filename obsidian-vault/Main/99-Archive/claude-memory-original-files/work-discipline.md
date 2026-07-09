---
name: work-discipline
description: Verification-first work habits -- always verify changes, root-owned files, no Caddy, browser-agent for demos
type: feedback
---

- **ALWAYS verify after every change** -- run a check immediately. Never assume it worked.
- Root-owned files in mounted volumes: edit via `docker exec` or `docker cp`, not from host.
- **NO Caddy** -- reverse proxy is **Cloudflare Tunnel** (`cloudflared` container).
- When presenting something to the user, use **browser-agent (Lightpanda only, NOT Playwright)** to verify it loads correctly before sharing the URL.

**Why:** Roberto caught multiple cases where changes were reported as done but hadn't actually taken effect, and where wrong assumptions about infrastructure (Caddy vs Cloudflare) led to wasted work.

**How to apply:** After any edit, immediately run a verification command. For Docker services: check logs. For files: read back. For UI: browser-agent screenshot.
