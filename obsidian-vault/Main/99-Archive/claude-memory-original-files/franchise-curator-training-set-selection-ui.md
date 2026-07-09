---
name: Franchise Curator - training set selection UI
description: Cloudflare-Access-gated web UI on franchise.synai.ai/curate for picking training images per character
type: project
---

Franchise Curator is the write-capable companion to franchise-viewer for the time-travel-franchise project. Lets Roberto curate (pick / approve) raw training images per character, with the canonical reference photo pinned beside the grid for side-by-side comparison.

## URLs

- Public viewer (read-only, no auth): https://franchise.synai.ai
- Curator picker: https://franchise.synai.ai/curate/  (Cloudflare Access gated)
- Per-character curator: https://franchise.synai.ai/curate/{character}/  e.g. /curate/joel/

## Architecture

Two containers behind one tunnel/domain:
- `franchise-viewer` (nginx:1.27-alpine, port 8080) — public read-only listings for /bible/, /stories/, /hero_refs/, /runs/, /training_sets/. Also reverse-proxies `/curate*` and `/api/curate*` to franchise-curator.
- `franchise-curator` (FastAPI 0.115 on python:3.12-slim, port 8085 internal) — writable. Lives at `~/commander/projects/franchise-curator/` with `main.py`, `Dockerfile`, `requirements.txt`, and `static/` (index.html, curate.html, style.css). The `static/` dir is bind-mounted at runtime for live CSS/HTML iteration without rebuild; main.py changes still need `docker compose build franchise-curator`.

Cloudflare:
- Tunnel routes `franchise.synai.ai` -> `franchise-viewer:8080` (unchanged).
- Cloudflare Access Application `<REDACTED-UUID-19>` ("Franchise Curator") with `destinations` scoped to `franchise.synai.ai/curate` and `franchise.synai.ai/api/curate` — path-based, NOT whole-domain (whole-domain breaks the public viewer).
- Policy `<REDACTED-UUID-20>` allows: robomello79@gmail.com and giseledutrasantos@gmail.com. 24h session. Google login + email OTP.

## Selection storage (non-destructive)

Per character, two small files live in `training_sets/{character}/`:
- `_selections.json` — `{character, version, main_image, selected: [filenames], updated_at}`. Approved raw filenames go here. Raw files stay in `raw/` untouched.
- `_main.txt` — optional pointer to which raw filename is the canonical reference. If absent, the curator defaults to the newest file in `raw/`.

Training pipelines should read `_selections.json` and symlink the listed files into a temp folder for ai-toolkit's `folder_path`, OR update the existing yaml configs (e.g. `joel_lora_qwen_v1.yaml`) to consume the manifest directly.

## UI behavior

Desktop: 320px sticky sidebar with full-size canonical reference + counter + bulk buttons; grid of thumbnails (minmax 180px) on the right.

Mobile (<=768px): compact sticky-top header with 128px reference on the left, counter + buttons on the right; 2-column grid below. <380px viewport drops to 1 column with even bigger thumbs; reference shrinks to 112px.

Interactions:
- Tap (or click) image -> toggle selection. Persists to `_selections.json` via `POST /api/curate/{char}/toggle`.
- Long-press 0.55s (or right-click on desktop) -> set as canonical main reference. Triggers `navigator.vibrate(40)` on supported phones.
- "Select all" / "Clear all" buttons -> `POST /api/curate/{char}/bulk`.
- Pinned reference always visible while scrolling, with blue ring (`--main-ring: #38bdf8`); selected items get green border (`--accent: #4ade80`); the current main image gets an inset blue glow.

## Cache strategy

HTML responses send `Cache-Control: no-store, no-cache, must-revalidate, max-age=0` AND `Clear-Site-Data: "cache"`. This means any reload after a deploy clears the browser's HTTP cache for the origin, so users never get stuck on old layouts. CSS link in the HTML also carries a `?v=<mtime>` query stamp for belt-and-braces invalidation. Reload at `/curate/joel/` always picks up new static assets without URL tricks.

## Endpoints

- `GET  /healthz` -> "ok"
- `GET  /api/curate/characters` -> all characters with raw/ dirs, plus raw_count and selected_count
- `GET  /api/curate/{char}/state` -> images[] with selected flag, main_image, main_url, counts
- `POST /api/curate/{char}/toggle` body `{filename, selected}` -> updates manifest
- `POST /api/curate/{char}/bulk` body `{selected: [filenames]}` -> sets entire selection
- `POST /api/curate/{char}/set_main` body `{filename, selected}` -> writes `_main.txt` and updates manifest
- `GET  /curate/{char}/` -> serves curate.html with `__CHARACTER__` token replaced
- `GET  /curate/static/{file}` -> CSS, JS, etc.

Character names are validated against `^[a-z][a-z0-9_-]{0,31}$`; filenames against `^[A-Za-z0-9._-]+$`. Concurrent writes guarded by an asyncio.Lock per character. JSON manifest writes are atomic via `_selections.json.tmp` -> rename.

## How to add a new character

Just create `~/commander/projects/time-travel-franchise/.state/training_sets/{newname}/raw/` and drop images in. It auto-appears in `/curate/`. No config change needed.

## Gotchas

- Bind-mounted nginx.conf gets a NEW inode on Edit (atomic rename), so franchise-viewer needs `docker compose stop && rm -f && up -d` (not just restart) when nginx config changes. Same with main.py if not bind-mounted.
- Cloudflare Access destinations array allows multiple URIs per app — use that for path scoping, NOT `domain` field (legacy). Whole-hostname apps break the public viewer.
- The auto-mode classifier may flag any "add user to access policy" call as a security warning even when the user explicitly authorized it; review the agent's actual action vs the warning.

## See also

- [[joel-lora-img2img-workaround-for-time-travel-franchise]] - workflow for face-locked image gen while waiting for the v2 LoRA retrain that will consume `_selections.json`
