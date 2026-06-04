# Handoff: Hank — rewire to local Qwen3-VL (OCR) + claude CLI (insights)

**Date**: 2026-06-03 20:54:37 (CDT / UTC-6)
**Project**: Mello Home Server (infra repo `/home/mello`) + Hank app (`/data/projects/hankbook/hank`, NOT a git repo)
**Branch**: master (`/home/mello` repo)
**Session Summary**: Reviewed the "Hank" receipt-to-books Next.js app, fixed 7 findings, dockerized it, and deployed it live at https://hank.synai.ai (demo mode). Then pivoted on Roberto's direction to make AI fully LOCAL: Qwen3-VL-32B for receipt OCR + `claude` CLI for insights. No ComfyUI, no cloud Gemini/Anthropic API, no Anthropic SDK. Paused mid-build with the vLLM service + hank env changes STAGED in docker-compose.yml but NOT applied.

## Completed This Session
- 7 code-review fixes to the Hank app (all uncommitted; app dir is not a git repo):
  - Rate limiting on AI routes: new `/data/projects/hankbook/hank/lib/ratelimit.ts` + `lib/guard.ts` (per-IP fixed window; verified 429 fires). Applied to `app/api/extract/route.ts` + `app/api/insights/route.ts`.
  - CSV formula-injection fix in `components/ExportPanel.tsx` (`csvCell` prefixes `= + - @ \t \r`).
  - `lib/ai.ts` `parseJson` now tries `JSON.parse` first, brace-scan fallback.
  - `lib/types.ts` `ExtractionSchema` made lenient (coerce + per-field `.catch`, confidence clamped 0..1).
  - `lib/format.ts`: added `round2` + `periodRange`; `money()` uses explicit guards (also fixed `$NaN`). `periodRange` used in `Dashboard.tsx` + `ExportPanel.tsx`.
  - `??`-over-`||` explicit guards in `Receipts.tsx` (amount/currency, media-type validation); PDF copy corrected.
  - `app/api/extract/route.ts`: media-type whitelist + 8MB payload cap.
- Dockerized: `Dockerfile` (multi-stage `node:20-alpine`, standalone, non-root), `.dockerignore`, `public/.gitkeep`, `next.config.mjs` `output: "standalone"`.
- `docker-compose.yml`: added `hank` service (image `hank:latest`, `127.0.0.1:3060->3000`, `n8n-net`, `TZ=Etc/GMT+6`, healthcheck on `http://127.0.0.1:3000/api/status`). Built + running.
- Live deploy: Cloudflare token-tunnel route `hank.synai.ai -> http://hank:3000` + proxied DNS CNAME (via cloudflare-agent; all 57 existing routes preserved). Verified HTTPS 200 + browser screenshot of the dashboard. **Currently DEMO MODE.**
- Fixed a healthcheck bug: container `localhost` resolves to `::1` (IPv6) but Next binds IPv4 `0.0.0.0`, so healthcheck must use `127.0.0.1`. `server-health-monitor` autoheal had been restart-looping it.
- Saved an Infrastructure memory to Obsidian (hank deployment + gotchas).

## In Progress
- [ ] (task #7) `qwen3-vl` vLLM service — **block ADDED to `docker-compose.yml` but NOT launched.** vllm/vllm-openai:v0.20.0, serves `/models/qwen3-vl` (mounted from `/home/mello/ComfyUI/models/LLM/Qwen-VL/Qwen3-VL-32B-Instruct`), `--dtype bfloat16 --enforce-eager --max-model-len 32768 --gpu-memory-utilization 0.92`, `device_ids: ['1']`, `shm_size 16gb`, `127.0.0.1:8064:8000`, `/health` healthcheck, `start_period 600s`. NEXT: `docker compose up -d qwen3-vl`, wait ~minutes for bf16 load, verify `/v1/models` + a vision `/v1/chat/completions` call.

## Pending (Not Started)
- [ ] (task #8) Rewrite `app/api/extract/route.ts`: replace Anthropic SDK vision call with `fetch` to `http://qwen3-vl:8000/v1/chat/completions` (OpenAI vision format: `messages` with `image_url` data URI + the existing `SYSTEM` extraction prompt + "Extract this receipt as JSON"). Keep rate limit, size/type guards, `parseJson`, `ExtractionSchema`, `coerceCategory`.
- [ ] (task #9) Rewrite `app/api/insights/route.ts`: replace Anthropic SDK with spawning `claude --print --model sonnet --append-system-prompt <SYS>` (txns JSON via stdin). Parse stdout via `parseJson` + `InsightsSchema`. Keep rate limit.
- [ ] (task #10) Strip `@anthropic-ai/sdk` from `package.json` + `lib/ai.ts`; remove `ANTHROPIC_API_KEY` + `GEMINI` usage. Add vLLM chat helper + claude-CLI runner to `lib/ai.ts`. Update `.env.example` (`VISION_API_URL`, `EXTRACT_MODEL=qwen3-vl`, `INSIGHTS_MODEL=sonnet`; drop ANTHROPIC/GEMINI). Update `README.md` + project `CLAUDE.md` stack notes.
- [ ] (task #11) `Dockerfile`: add `RUN npm i -g @anthropic-ai/claude-code` in runner stage. `docker-compose.yml` `hank`: mount `/home/mello/.claude.json` (+ likely `~/.claude/`) into the container, set `HOME`, env `VISION_API_URL=http://qwen3-vl:8000/v1`, drop the env_file/ANTHROPIC/GEMINI, `depends_on: qwen3-vl`. Rebuild image + recreate.
- [ ] (task #12) E2E verify: synthetic receipt -> `/api/extract` (Qwen3-VL) returns structured JSON; `/api/insights` returns flags via claude CLI; browser screenshot of hank.synai.ai; confirm VRAM stable on `device_ids ['1']`.

## Blockers
- None. (Pause is voluntary; nothing half-applied.)

## Key Decisions Made
- **Receipt OCR = local Qwen3-VL-32B-Instruct (bf16) via a dedicated vLLM**, not ComfyUI and not cloud. Reasoning: Roberto's rules keep Vision/OCR local-only and ban Gemini; "we use the LLM directly" (not ComfyUI's workflow layer). vLLM 0.20 confirmed to support `Qwen3VLForConditionalGeneration`.
- **Insights = `claude` CLI** (`claude --print --model sonnet`), not the Anthropic API/SDK. Matches the CLI-only rule. Requires mounting `claude` + `.claude.json` into the container.
- **GPU placement: `device_ids: ['1']`** = the 600W Workstation card (bus 29, UUID `fdfcedb7`), which was ~96GB free after nemotron was removed. Confirmed by the updated `context.md`: `['1']` = Workstation (PRIMARY), `['0']` = Max-Q (300W secondary). New policy pins single-GPU services to `['1']`.
- **Drop the Gemini key and the cloud Anthropic key** from Hank entirely once local wiring lands.

## Known Issues
- Staged `hank` `env_file` edit is now STALE: `docker-compose.yml` `hank` currently has `env_file: /data/projects/hankbook/hank/.env` + the `ANTHROPIC_API_KEY` env line removed (from the earlier cloud-Claude attempt). The local plan does NOT use that key — task #11 must replace this (VISION_API_URL + claude CLI mount, no anthropic/gemini).
- `/data/projects/hankbook/hank/.env` contains a VALID `ANTHROPIC_API_KEY`, plus `EXTRACT_MODEL`, `INSIGHTS_MODEL`, `GEMINI`, `PROJECT_NAME`, `PROJECT_NUMBER`. Not used by the local plan; decide whether to keep any as fallback (likely remove).
- vLLM image has no `curl`/`wget`; healthcheck uses `python3 -c urllib` (python3 at `/usr/bin/python3`).

## Next Steps (Priority Order)
1. Launch `qwen3-vl` (`docker compose up -d qwen3-vl`) FIRST — the bf16 load takes minutes; let it warm while doing app code. Watch `docker logs qwen3-vl` for "Application startup complete"; verify `curl 127.0.0.1:8064/v1/models`.
2. Rewrite the two Hank routes (extract -> Qwen3-VL OpenAI vision; insights -> claude CLI) + `lib/ai.ts` + remove the SDK (tasks #8/#9/#10).
3. Dockerfile claude CLI + compose mounts/env + rebuild + recreate (task #11), then E2E verify (task #12).

## Files Actively Being Edited
- `docker-compose.yml` (in `/home/mello` repo) — `qwen3-vl` service ADDED (not launched); `hank` service has a stale `env_file` edit to revisit. UNCOMMITTED.
- `/data/projects/hankbook/hank/app/api/extract/route.ts` — fixes applied; NEXT to be rewritten for Qwen3-VL.
- `/data/projects/hankbook/hank/app/api/insights/route.ts` — fixes applied; NEXT to be rewritten for claude CLI.
- `/data/projects/hankbook/hank/lib/ai.ts` — `parseJson` fixed; NEXT to drop Anthropic SDK, add vLLM + CLI helpers.
- `/data/projects/hankbook/hank/Dockerfile` — standalone build; NEXT to add claude CLI.
- Also already-edited: `lib/types.ts`, `lib/format.ts`, `lib/ratelimit.ts`, `lib/guard.ts`, `components/{ExportPanel,Dashboard,Ledger,Insights,Receipts}.tsx`, `next.config.mjs`, `.dockerignore`, `public/.gitkeep`.

## Context for Next Session
- App source: `/data/projects/hankbook/hank` (extracted from `hank-app.zip`; NOT git-tracked). Infra: `/home/mello/docker-compose.yml` (git repo `master`).
- Live now: https://hank.synai.ai = DEMO MODE, `hank` container healthy, `127.0.0.1:3060->3000`, on `n8n-net`. Untouched by the staged compose edits (no `docker compose up` run since).
- GPU device map (verified by UUID + confirmed in context.md): `device_ids ['0']` = Max-Q 300W (bus 27, UUID `36155eda`, ~89GB free, ~8GB used by comfyui/ffmpeg/ollama). `device_ids ['1']` = Workstation 600W (bus 29, UUID `fdfcedb7`, ~96GB free). Inside a single-GPU container the card appears as `cuda:0`.
- vLLM image entrypoint is `["vllm","serve"]`, so compose `command:` = `[model_path, --flags...]`.
- Qwen3-VL-32B dir has full HF files (config/tokenizer/preprocessor/chat_template) — vLLM-loadable, model_type `qwen3_vl`, arch `Qwen3VLForConditionalGeneration`.
- `claude` CLI: `/home/mello/.local/bin/claude` v2.1.162; `/home/mello/.claude.json` present. Container gotcha: mount `.claude.json` (else empty output, exit 0; check `~/.claude/debug/latest`).
- `server-health-monitor` is an autoheal that restarts `unhealthy` containers — keep healthchecks correct + generous `start_period` (vLLM uses 600s).
- Cloudflare: token tunnel; creds in `/home/mello/.env` (ACCOUNT_ID, API_TOKEN, ZONE_ID, TUNNEL_ID). API token cannot read zone settings (err 9109). `hank.synai.ai` route already live.
- Hank has a working DEMO fallback (sample data + local heuristic insights) independent of any AI engine.
- Task list IDs #7-#12 track the remaining work (TaskList).

## Git State
- Branch: master (`/home/mello`)
- Last commit: 6c23932 "feat(agent-flow): join claudicle_default network for cost enrichment"
- Uncommitted changes: `docker-compose.yml` (added `qwen3-vl` service + `hank` service with stale env_file edit). Hank app changes live under `/data/projects/hankbook/hank` which is NOT a git repo (not tracked anywhere).
