---
name: Skool Comment-Reply Pipeline (skool-api + skool-reply)
description: Skool community engagement system: skool-api FastAPI/Playwright scraper + host-side cron orchestrator + skool-reply dashboard with Cloudflare Access
type: project
---

# Skool Comment-Reply Pipeline

Live, end-to-end engagement system for Skool communities. **No n8n** — host-side Python cron + containerized FastAPI scraper + web dashboard. **Mode: human review** — drafts wait for click; no autonomous posting.

## Architecture

```
cron (user mello, host)
       |
       v
 pipeline/run_daily.py  --HTTP-->  skool-api :8091  --Playwright--> skool.com
       |                                /feed
       |  claude --print --model haiku   /post/scrape
       |  (host subprocess)              /post/engage
       v
 NocoDB Skool Replies (m6uf5mi5mw4wr1s) <--reads-- skool-reply :8092 --> skool-reply.synai.ai (CF Access)
                                                  (reads shared config.json)
```

## Services / Ports

| Service | Port | Domain |
|---|---|---|
| skool-api (FastAPI + Playwright) | 127.0.0.1:8091 | (internal only) |
| skool-reply (FastAPI + Jinja dashboard) | 127.0.0.1:8092 | https://skool-reply.synai.ai |

Both bound to loopback; the dashboard goes public via the existing token-managed `cloudflared` container (public hostname added in Cloudflare Zero Trust dashboard, not a file).

## Key Files

- `/home/mello/commander/projects/skool-api/` — image `skool-api:latest`, user 1001:1001, on `n8n-net`
  - `app/main.py` — FastAPI endpoints (`/feed`, `/post/scrape`, `/post/engage`, `/notifications`, `/prompts*`, `/group-settings`, `/posts/ignore`)
  - `app/scraper.py` — `SkoolScraper` with `scrape_feed`, `scrape_post`, `engage_post`; lifted JS blobs `FEED_JS`, `EXTRACT_JS`, `STATE_JS`, `LIKE_ALL_JS`, `SUBMIT_JS` from the proven spike scripts
  - `app/scheduler.py` — APScheduler heartbeat (5min) + notif poll (15min)
  - `app/database.py` — NocoDB writes via `nocodb_client.NocoDBClient`
- `/home/mello/commander/projects/skool-api/pipeline/` (host orchestrator)
  - `config.json` — shared with the dashboard (`daily_cap`, `shadow_mode`, `time_window`, `communities[]`)
  - `system_prompt.txt` — Haiku comment-generation system prompt (1-2 sentences, no exclamations, no emojis, don't start with "I", don't name the community)
  - `run_daily.py` — orchestrator; `fcntl.flock` on `/tmp/skool_run_daily.lock`; runs in its own `.venv`
- `/home/mello/commander/projects/skool-reply/` — dashboard
  - Mounts the pipeline dir read-write so both the dashboard and orchestrator read/write the same `config.json` + `system_prompt.txt` (atomic write-temp + `os.replace`)
  - Dark theme, no JS framework; routes `/` (communities), `/replies`, `/settings`, `/api/healthcheck`

## Cookies & Auth

- Cookies in `/home/mello/.cookies/skool.json`, mounted read-only at `/app/cookies` inside skool-api
- skool-api endpoints are **unauthenticated** but bound to 127.0.0.1 only and never tunneled
- The dashboard hostname is the only public surface, gated by Cloudflare Access (Google)
- Roberto's Skool handle: `roberto-de-mello-8666`

## NocoDB Schema

- Base `ph5ghfzrkyg3yvy`, table `m6uf5mi5mw4wr1s` (Skool Replies)
- Columns: `group_slug`, `post_slug`, `post_id`, `post_title`, `trigger` (`proactive_comment` / `comment_on_my_post` / `reply_to_my_comment`), `parent_comment_id`, `parent_comment_text`, `reply_text`, `our_comment_id` (left blank — never reliably extracted), `status` (`posted`/`shadow`/`failed`/`skipped`), `error`, `generated_at`, `posted_at`
- NocoDB hostname differs by caller: host orchestrator -> `https://nocodb.synai.ai`; container dashboard -> `http://nocodb:8080`

## Dedupe & Safety

- Per-post dedup: NocoDB query `where=(post_id,eq,X)~and(status,anyof,posted,shadow,skipped)` — `failed` rows do NOT block (retryable)
- Daily-cap pre-check counts today's `posted` rows by `posted_at >= today_midnight_utc-6` so multiple cron firings are idempotent
- Own-post guard: skips when scraped `author_handle == community.own_handle` (writes `skipped` row, `error=own_post`)
- Single-instance file lock `/tmp/skool_run_daily.lock` so overlapping cron firings can't double-post
- Comment validation rejects: >320 chars, emoji, `!`, starts with "I "/"I'", contains "creator university"/"acu". One regeneration retry on failure
- `shadow_mode: true` is the default — generates + logs but never posts; flipped via the dashboard's `/settings` page

## Scheduling

```cron
0 10,16 * * * cd /home/mello/commander/projects/skool-api/pipeline && .venv/bin/python run_daily.py >> pipeline.log 2>&1
```

Two firings/day with `daily_cap=3` and the idempotent pre-check: first run posts up to 3, second tops up if the first under-delivered.

CLI flags on `run_daily.py`: `--shadow`, `--live`, `--community <slug>`, `--dry-run`.

## Currently Done (production-verified)

- Likes ride-along (`_like_post_on_page` + `LIKE_POST_JS`): after approving a reply, the post is liked, own posts skipped
- Per-post ignore: `database.py set_post_ignored` + `POST /posts/ignore` + Ignore/Unignore buttons + `Ignored` tab
- Mobile redesign: `base.html` `@media (max-width:720px)` → stacked cards on phones; desktop table intact
- `skool-reply.synai.ai` tunnel live behind CF Access
- Per-community on/off toggle on `/`
- Author filter `<select>` on group view
- Healthcheck fix: replaced `curl` (not in slim Python image) with Python urllib one-liner

## Known Limitations / Out-of-Scope (Phase 1)

- `our_comment_id` always blank — the spike never extracted it reliably; dedupe keys on `post_id`
- Reply-to-comment triggers (`comment_on_my_post`, `reply_to_my_comment`) not built — `proactive_comment` only
- Notification relevance triage **blocked on Roberto's relevance rule** — Skool feed has no reply-to-post event (only new-post / admin-post / upvote), so the rework is "pull all notifications, AI judges each, surface relevant ones"
- Adding communities is a `config.json` edit, not a UI flow

## Lessons (already in memory under different titles)

- Skool group discovery uses `https://api2.skool.com/self/groups?limit=100`, NOT `pageProps.self.allGroups` (which truncates) — see #src-skool-reply-pipeline-group-discovery-uses-self-groups-not-allgroups
- skool-api is a slim Python image with no Claude CLI — comment generation has to run on the host
- Empty stdout + exit 0 from `claude --print` inside containers is the documented Docker/Claude gotcha — treat empty stdout as failure
