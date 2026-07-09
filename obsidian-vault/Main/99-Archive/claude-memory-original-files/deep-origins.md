---
name: Deep Origins
description: Evolutionary video pipeline with dashboard at origins.synai.ai — LangGraph + Flux 2 + Kling v2.1-pro, species name in / video out
type: project
originSessionId: <REDACTED-UUID-10>
---
Roberto's autonomous agentic system that turns a species name into a full evolutionary timeline video.

**What it does:** Research lineage (LLM) → human approval gate → Flux-2 image per species → Gemini QA → Kling v2.1-pro morph videos → Suno music → FFmpeg stitch → publish to YouTube/Facebook/TikTok. Budget cap $15/video, SQLite checkpointer so restarts resume mid-job.

## Location & access
- **Path:** `/home/mello/commander/projects/deep-origins/`
- **Container:** `deep-origins` on `n8n-net`, port `127.0.0.1:8060:8060`
- **Domain:** `https://origins.synai.ai` — gated by **CF Access** (Google OAuth + email OTP for robomello79@gmail.com).
  - CF Access app UUID: `<REDACTED-UUID-11>`
  - Policy UUID: `<REDACTED-UUID-12>`
- **Persistence:** `/data/sites/deep-origins/` (bind-mounted via `/data/sites` in compose)
  - `jobs_index.json` — sidecar with job metadata for dashboard listing
  - `checkpoints.db` + `-wal` + `-shm` — AsyncSqliteSaver LangGraph state

## Dashboard (2026-04-24)
Built lux-style UI in same session as CF-Access rollout. Pages:
- `/` — create-job form + live jobs panel (3s polling, running/recent split, header pill)
- `/jobs/{id}` — detail with progress bar, stage text, species list, approve/reject buttons when `awaiting_approval`, final video link
- `/login` — in-app cookie auth (redundant behind CF Access, but kept as defense-in-depth; paste `DEEP_ORIGINS_API_KEY` from env)
- `/logout` — clears the cookie

## API
- JSON under `/api/jobs*`: `POST /api/jobs`, `GET /api/jobs/{id}`, `POST /api/jobs/{id}/approve`, `GET /api/jobs/{id}/species`, `GET /api/jobs/{id}/morphs`, `GET /api/jobs-summary`
- Legacy `/jobs*` POST + sub-routes kept for backward compat. `GET /jobs/{id}` is now HTML (breaking change for old JSON clients — update them to `/api/jobs/{id}`).
- Auth: accepts `x-api-key` header OR `do_session` cookie; inner auth is in addition to CF Access gate.

## Gotchas
- Starlette 1.0 uses `TemplateResponse(request, "name.html", ctx)` not the old `("name.html", {"request":..., ...})`. Getting it wrong throws `TypeError: unhashable type: 'dict'` in Jinja cache lookup.
- `_pipeline_app` must be lazy-initialized behind an `asyncio.Lock()` — uvicorn workers race on first request otherwise.
- `pipeline.create_app` is now async (uses `AsyncSqliteSaver` over aiosqlite). CLI `run` subcommand uses `create_app_sync` wrapper.
- `/data/sites/deep-origins/` gets root-owned files because the container runs as root. If Roberto needs to edit from host, `sudo chown mello:mello -R /data/sites/deep-origins` after changes.
- Original `SqliteSaver` reference in `agents/pipeline.py:735` was undefined (never imported) — pre-existing bug, surfaced only when I started exercising the pipeline from the dashboard. Fixed to `AsyncSqliteSaver`.

## Related memory
- [Cloudflare Access](cloudflare-access.md) — tokens, tunnel ID, policy patterns used for this rollout
- [Luxurious Cabins](luxurious-cabins.md) — the sibling pipeline whose dashboard pattern was mirrored here
