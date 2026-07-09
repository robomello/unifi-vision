---
name: Hank app deployed at hank.synai.ai
description: Hank receipt-to-books Next.js app live at hank.synai.ai in demo mode; includes Next-standalone healthcheck + autoheal gotchas
type: project
---

**Hank** = receipt-to-books Next.js 14 app for trade contractors. Source: `/data/projects/hankbook/hank` (extracted from hank-app.zip).

Deploy:
- Docker service `hank` in `/home/mello/docker-compose.yml` (image `hank:latest`, Next "standalone" multi-stage node:20-alpine, non-root).
- Bind `127.0.0.1:3060->3000`, network `n8n-net`, `TZ=Etc/GMT+6`.
- Cloudflare token tunnel: ingress `hank.synai.ai -> http://hank:3000` (added via API, all 57 existing routes preserved); DNS CNAME `hank` -> `<tunnel>.cfargotunnel.com` proxied.
- **Demo mode**: `ANTHROPIC_API_KEY` is empty in `/home/mello/.env`, so live receipt scanning is off (sample data + local heuristic review still work). Passed as `${ANTHROPIC_API_KEY:-}`; set a real key in `.env` then `docker compose up -d hank` to enable live Haiku 4.5 extraction + Sonnet 4.6 insights. No usable Anthropic API key on this box (CLI/subscription only).
- AI routes now rate-limited (`EXTRACT_RATE_LIMIT=20`, `INSIGHTS_RATE_LIMIT=10` per IP/min) since there's no auth yet.

Reusable gotchas (cost real debugging time):
- Next.js `output: "standalone"` server binds IPv4 `0.0.0.0` only. A container HEALTHCHECK using `http://localhost:3000` fails because container `localhost` resolves to `::1` (IPv6) first -> connection refused. Use `http://127.0.0.1:3000`.
- `server-health-monitor` is an autoheal: it restarts any container marked `unhealthy`, so a bad healthcheck causes a restart loop, not just a red status.
