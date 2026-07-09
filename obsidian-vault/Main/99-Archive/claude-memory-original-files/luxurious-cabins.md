---
name: Luxurious Cabins
description: Local home-tour video pipeline replacing the old Airtable+n8n+cloud-models setup. FastAPI at luxurious-cabins.synai.ai + home-tours.synai.ai, NocoDB-backed, multi-engine A/B testing.
type: project
originSessionId: <REDACTED-UUID-22>
---
Roberto's local-only rebuild of the home-tour video pipeline. Previous pipeline used Airtable + n8n + MidJourney/Gemini/ElevenLabs and stalled on ~90% of jobs post-generation. Rebuild is fully local (plus optional Nano Banana 2 via Fal.ai as a visual-quality baseline).

**Why:** Old pipeline cost money per video (cloud models), stalled often, and the `Home Styles` dropdown was dead. New pipeline targets $0 per video when using local engines and gives a live UI instead of Airtable.

**How to apply:** When Roberto references "home tours", "luxurious cabins", or the Airtable home-tour pipeline — this IS that project. The old `/home/mello/commander/projects/home-tour-gen/` directory was renamed to `luxurious-cabins/` on 2026-04-22.

## Location & access
- **Path:** `/home/mello/commander/projects/luxurious-cabins/`
- **Container:** `luxurious-cabins` on `n8n-net`, port `127.0.0.1:8071:8071`
- **Domains (both live, both gated by CF Access with Google OAuth + email OTP for `robomello79@gmail.com`):**
  - Primary: `https://luxurious-cabins.synai.ai`
  - Alias: `https://home-tours.synai.ai` (legacy; user kept working during rename)
- **CF Access app UUIDs:** luxurious-cabins=`<REDACTED-UUID-23>`, home-tours=`<REDACTED-UUID-24>`
- **Output dir:** `/data/sites/evolution/home-tours/{job_id}/` (kept the old path to avoid moving in-flight jobs)
- **Public video URL prefix:** `https://videos.evolutionlabs.blog/home-tours/{job_id}/final.mp4`

## NocoDB
- **Base ID:** `ph5ghfzrkyg3yvy`
- **Tables:** `home_tour_jobs` (`mwqfkvvi3stlpi6`) + `home_tour_generations` (`m77lbcd834ysahi`) — names kept from rename for data stability
- **Non-obvious schema detail:** generations use a `job_ulid` plain-text column (NOT the NocoDB Link `job_id`) for filtering — the Link column can't be `where=(eq,...)` filtered, so the Python client uses the plain-text sidecar.

## Engines wired in
- **Image (3):** Qwen Image 2512 (default), Flux 2 Dev, Nano Banana 2 (Fal.ai — only cloud engine)
- **Video (6, all models on disk):** LTX-2.3 Distilled (default), LTX-2.3 Dev, Wan 2.2 I2V 14B, Wan 2.2 Lightspeed (Dasiwa), HunyuanVideo 1.5 I2V, Kandinsky 5 Lite (T2V only)
- **Room plan + describe:** **Opus 4.7 vision via Claude CLI** (replaced QwenVL 8B on 2026-04-22 evening — QwenVL was bottlenecking the ComfyUI queue and producing weaker prompts). Implementation: `engines/llm.describe_and_plan` uses `claude --print --model opus --add-dir {image_dir} --allowedTools Read` and `@`-references the start image. Single call returns JSON plan (title, house_style, 5 rooms). `--json-schema` flag silently returns empty output — use prompt-enforced JSON instead.
- **TTS:** ComfyUI-FishAudioS2 custom node (avoids a separate TTS service)
- **Foley:** hunyuanvideo-foley custom node for ambient audio per clip

## Status as of 2026-04-22 (evening)
- Rename from `home-tour-gen` → `luxurious-cabins` complete and verified live.
- Live jobs dashboard deployed on home page: running cards + header pill + 3s polling. Data handoff: `/api/jobs-summary`.
- Describe + plan migrated from QwenVL (local, ComfyUI-serialized) to Opus 4.7 vision (Claude CLI, parallel-safe). Smoke test: ~55s for 5-room plan from an exterior image.
- 7/8 pipeline stages work end-to-end (smoke test job `01KPQTM9BC55XAF6WKYQ5WXB9R` previously reached video stage).
- **Blocker (task #4):** needs ComfyUI API-format workflow JSONs exported for video engines + TTS + Foley. Must title-prefix parameterizable nodes with `IN:image`, `IN:prompt`, `IN:frames`, `IN:seed` for the generic runner.
- Rebuild gotcha: `docker compose build && up -d` recreates the container and kills any in-flight asyncio pipelines — surviving jobs freeze at their last DB status. Use the new dashboard's "↻ Restart" button per job after rebuild.
- Phase 0.5 video-engine shoot-out not yet run — queued behind workflow capture.

## Gotchas (already fixed, don't redo)
- Ollama host-level broken (gemma3/gemma4/qwen2.5vl/llama3.2 all fail) — sidestepped by routing room-plan JSON through QwenVL 8B, then later replaced entirely by Opus 4.7 vision.
- Only GPU 1 exposed to ComfyUI (`DeviceIDs=['1']`); v1 runs sequential on one GPU despite plan mentioning dual-GPU parallelism.
- `AILab_QwenVL` node caps `max_tokens` at 2048 (not 3000) — no longer relevant for describe/plan since Opus runs off-GPU.
- UI-format ComfyUI workflow JSONs can't be `POST /prompt`'d — API-format export required (the capture blocker above).
- Claude CLI `--json-schema` returns empty output for complex schemas on Opus 4.7 — rely on prompt-enforced JSON ("Return ONLY a JSON object, first char `{`, last char `}`") instead.
- Claude CLI in container runs as root; host `.claude/settings.json` has `defaultMode: bypassPermissions` which is rejected for root — always pass `--permission-mode default` explicitly.
- For Opus vision in print mode, `@/path/image.png` works only with `--add-dir <dir>` + `--allowedTools Read` (Read tool invocation needs explicit permission under `--permission-mode default`).

## Related memory
- [Active Projects](active-projects.md) — also lists this project (renamed entry)
- [Cloudflare Access](cloudflare-access.md) — how the Google OAuth + email OTP policy pattern works
- [Docker GPU Config](docker-gpu-config.md) — ComfyUI GPU 1 pinning
