---
name: Luxurious Cabins — Resumable Pipeline Architecture
description: Per-stage NocoDB status columns, stuck/degraded job states, resume() replaces restart() (no auto-wipe), image/voice/video/foley short-circuit logic, known Docker-rebuild caveat
type: project
---

# Luxurious Cabins — Resumable Pipeline

Pipeline at `/home/mello/commander/projects/luxurious-cabins/` was refactored from "any stage failure wipes everything and re-renders from scratch" → "any stage failure freezes the job; Restart resumes only the failed stages, reusing files already on disk."

## Triggering Incident

Job rendered room 0 image (2 MB on disk), then TTS failed (`/data/audio/refs/home-tours.wav` missing — caught, continued), then video stage raised `ComfyUIError: workflow video_ltx23_distilled.json not found`. Old `_run_pipeline` set `status=failed`, slept 5s, called `restart()` which DELETED all 5 generation rows and re-ran describe+plan+image — user watched the same image render twice and get thrown away.

## NocoDB Schema Additions

**`home_tour_generations`** (6 new cols, all SingleLineText except `last_error`):
| Column | States | Default |
|---|---|---|
| `image_status` | pending\|running\|done\|failed | pending |
| `voice_status` | pending\|skipped\|running\|done\|failed | pending |
| `video_status` | pending\|running\|done\|failed | pending |
| `foley_status` | pending\|skipped\|running\|done\|failed | pending |
| `last_error` | LongText (1500-char truncated) | null |
| `last_failed_stage` | image\|voice\|video\|foley | null |

The existing `status` column on generations is now a **derived rollup** written by `_recompute_row_status()` — remains the coarse "what's this row doing right now" for dashboard current-room detection. Backward compatible (reader code defaults absent fields to `"pending"`).

**`home_tour_jobs`** (2 new cols):
- `restart_count` (Number, default 0)
- `last_restart_at` (DateTime, nullable)

Migration script: `scripts/add_resume_columns.py` (idempotent — GETs columns first, skips existing).

## Job Status Ladder (expanded)

| Status | Meaning |
|---|---|
| `queued` | Row exists, pipeline task not yet running |
| `describing` | Opus describe+plan running |
| `generating_rooms` | In per-room loop |
| `assembling` | All rooms done through video, running ffmpeg concat |
| `published` | Success — all rooms have `video_status=done` |
| `degraded` | Pipeline walked but ≥1 non-blocking stage failed (voice/foley) — "done but incomplete" |
| `stuck` | Pipeline paused mid-run because a blocking stage failed. Manual Restart required. (NEW — distinguishes "resumable GPU-stage failure" from `failed`.) |
| `failed` | Reserved for true unrecoverable bugs: Opus returned no rooms, start image missing, assemble itself crashed |

`BLOCKING_STAGES = {"image", "video"}` → failure marks job `stuck`.
`NON_BLOCKING_STAGES = {"voice", "foley"}` → failure marks row, pipeline continues, job ends `degraded`.

## resume() Replaces restart()

The HTTP endpoint `/api/jobs/{id}/restart` is preserved (user mental model + button label), but the internal function is now `resume(job_id)`:

1. Demotes any `failed` stage statuses back to `pending` (so `_run_room` retries them)
2. Leaves `done` stages alone (path-existence check inside `_run_room` handles missing files)
3. Clears `last_error` + `last_failed_stage`
4. Increments `restart_count`, sets `last_restart_at`
5. Sets job `status=queued`, error=""
6. `asyncio.create_task(_run_pipeline(job_id))`

**`delete_generations_for_job` is no longer called by app code** — kept in `nocodb.py` as a manual-rescue tool.

## Auto-Retry Removed

Old code had `MAX_AUTO_RETRIES = 1` + `_RETRY_COUNT` module dict. **Deleted entirely.** Rationale: old retry semantics were "wipe + retry" (rejected). Keeping "retry without wiping" is redundant with the per-stage short-circuit — transient hiccups leave job `stuck`, user clicks Restart. Anything that auto-retries hides real problems.

## Per-Stage Short-Circuit Logic (the heart of resume)

`_run_room` for each stage:
1. If `stage_status == "done"` AND output file exists → skip (reuse)
2. If `stage_status == "done"` but file missing → log, re-run
3. Otherwise: set `running`, attempt, on success set `done` + path, on failure either:
   - **Blocking** (image/video): set `failed` + `last_error` + `last_failed_stage`, raise `_BlockingStageFailure` → outer `_pipeline` catches, sets job `stuck`, returns (no further rooms processed)
   - **Non-blocking** (voice/foley): set `failed` + log warning, continue with `None` for that path

If all stages on entry are `done`/`skipped`, the room no-ops — zero GPU work on resume.

## Foley Path Limitation (deferred)

Foley outputs are not persisted on the generation row — assemble receives foley via in-memory tuple. On resume we trust `foley_status=done` and skip re-render, but we **cannot re-feed the file into assemble if workdir was nuked**. Operator guidance: don't `rm -rf` job dirs between runs. Adding a `foley_path` column is a 1-line migration if needed.

## Dashboard: Per-Room Stage Grid

`templates/index.html` renders for each room: thumbnail + room name + compact stage icons (`i✓ v✓ c✗ f·` — first letter + state icon `✓ … · ✗ –`). Stuck/degraded jobs stay in the running bucket (`STUCK_STATUSES = {"stuck", "degraded"}` — separate from `ACTIVE_STATUSES`) so user sees where the job paused and the Restart button.

Restart confirm copy: "Resume this job? Already-rendered images and clips will be reused; only failed or missing stages will run again."

New media endpoint `/jobs/{job_id}/media/{room_idx}/{kind}` with path-traversal guard via `path.relative_to(job_dir.resolve())`.

## Known Caveat — Docker Rebuild Kills In-Flight Tasks

`docker compose up -d --build` kills in-flight asyncio tasks. Jobs in `describing`/`generating_rooms`/`assembling` will be visible in NocoDB but no worker is running them — they appear stuck forever.

**Workaround**: manually mark them `stuck` via NocoDB UI and click Restart; per-stage short-circuit resumes from filesystem-persisted work.

**Proper fix (separate plan)**: boot-time sweep in `server.py` startup that finds jobs with status in `{describing, generating_rooms, assembling}` and demotes them to `stuck`.

## File Touch Map

| File | Change |
|---|---|
| `orchestrator.py` | ~200 lines (near full rewrite of body) — new `_run_room`, `_pipeline` flow, `resume()`, `_recompute_row_status`, `_BlockingStageFailure` |
| `engines/nocodb.py` | +6 lines (new `get_generation(gen_id)`) |
| `server.py` | ~50 lines (imports, `summarize` per-room grid, new media endpoint) |
| `templates/index.html` | ~70 lines (stage-grid helpers, `renderRunning`, restart confirm) |
| `templates/base.html` (or inline) | ~40 lines CSS |
| `scripts/add_resume_columns.py` | new ~60 lines |

See parent project context: [[luxurious-cabins]].
