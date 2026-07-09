---
name: Pingvin Share file-sharing service
description: Public account-free file sharing at share.synai.ai (Pingvin Share Docker)
type: project
---

**Pingvin Share** deployed 2026-06-24 — public, account-free file sharing.

- **URL**: https://share.synai.ai (Cloudflare tunnel route + DNS via cloudflare-agent; no Access policy, public by design).
- **Container**: `pingvin-share` (image `stonith404/pingvin-share:latest`), in `docker-compose.yml`, network `n8n-net`, host debug port `127.0.0.1:3017:3000`. Data bind mount `/data/pingvin-share` (SQLite `pingvin-share.db` + `uploads/`).
- **Access model**: anyone uploads WITHOUT login (`allowUnauthenticatedShares=true`); downloads gated only by an optional per-share password the uploader sets (recipient enters password → cookie `share_<id>_token` → download; no account).
- **Abuse guards**: maxSize 3 GB, maxExpiration 7 days.
- **Admin**: account `mello_roberto@hotmail.com` (Roberto owns; temp password set at deploy, change on first login). Admin only needed for global config.
- **CONFIG GOTCHA**: Pingvin config is stored in the SQLite `Config` table (`category`,`name`,`value`,`defaultValue`), NOT env vars (only `TRUST_PROXY` is env). `value=NULL` means it falls back to `defaultValue`. The admin UI writes the `value` column; `updatedAt` is epoch-ms integer. No `sqlite3` binary on host/container — edit via `python3` sqlite3 module with sudo. Must `docker compose restart pingvin-share` (NOT bare `docker restart` — blocked by docker-compose-enforcer hook) to reload config.
- **Share API flow** (unauth): POST /api/shares (id,name,expiration like "7-days",security.password) → POST /api/shares/:id/files?name=&chunkIndex=0&totalChunks=1&id=<UUID> (file id MUST be a UUID) → POST /api/shares/:id/complete. Download: POST /api/shares/:id/token {password} → token, then GET /api/shares/:id/files/:fileId?download=true with cookie `share_<id>_token=<token>`.
- Upstream `stonith404/pingvin-share` archived 2025-06-29; maintained fork is "Pingvin Share X" (future-update note).
