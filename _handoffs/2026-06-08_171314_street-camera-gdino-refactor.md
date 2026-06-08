# Handoff: Street Camera — YOLO→Grounding DINO + gemma3:4b + GPU Migration

**Date**: 2026-06-08 17:13:14 (UTC-6)
**Project**: mello home server (docker-compose.yml + commander/projects/street-camera/)
**Branch**: master (root repo) / master (commander repo)
**Session Summary**: Diagnosed slow internet (server was fine; client-side spike). Fixed GPU pinning for street-camera/ollama-embed (wrong GPU). Refactored street-camera from YOLO11m+qwen2.5vl:7b to Grounding DINO+gemma3:4b — built, deployed, confirmed running.

## Completed This Session

- **GPU pinning fixed**: `street-camera` and `ollama-embed` were both pinned to GPU 0 (Max-Q 300W secondary). Moved both to `device_ids: ['1']` (600W primary). (uncommitted in root repo — `docker-compose.yml`)
- **street-camera: YOLO → Grounding DINO**: Replaced `ultralytics` YOLO11m with `IDEA-Research/grounding-dino-base`. Custom detection prompt: `"car . truck . delivery van . bus . motorcycle . person . dog . cat . bird ."` — delivery vans now a first-class label. (uncommitted in commander repo)
- **street-camera: qwen2.5vl:7b → gemma3:4b**: VLM switched from `ollama-embed:11434` to `ollama:11434` with `gemma3:4b` (vision confirmed). `think: false` added to payload. (uncommitted in commander repo)
- **New Dockerfile**: Switched base from `ultralytics/ultralytics` to `nvidia/cuda:12.8.0-devel-ubuntu24.04` + cu130 torch + transformers>=4.40 (mirrors ViQA's proven Blackwell sm_120 build). (uncommitted in commander repo)
- **GDINO weights cached**: First run auto-downloaded to `/home/mello/.cache/street-camera-hf/` (mounted as `/root/.cache`). Future restarts are instant.
- **gemma3:4b pulled**: Into main `ollama` container volume. Vision-capable confirmed (`ollama show` shows `vision` capability).
- **Service deployed and running**: All 4 cameras streaming, NVDEC open, 3 VLM workers ready, GDINO initialized on GPU 1.

## Pending (Not Started)

- [ ] **Commit all changes** — `docker-compose.yml` (root repo) + 4 street-camera files (commander repo) not yet committed
- [ ] **Tune confidence thresholds** — `GDINO_BOX_THRESHOLD=0.35` and `MIN_CONFIDENCE=0.45` are starting points; may need adjustment once live detections come in (GDINO sigmoid scores differ from YOLO's). Tune via env, no rebuild needed.
- [ ] **Verify first live vehicle detection** — wait for a car/truck to appear in camera view and confirm: (a) detection logged, (b) VLM returns non-default color/brand, (c) snapshot bbox is sane, (d) `docker logs ollama` shows gemma3 chat call (not ollama-embed)
- [ ] **GPU migration for other services** — most services still pin `device_ids: ['0']` (Max-Q). Policy says they should be on `['1']`. Migration noted as pending in context.md.

## Key Decisions Made

- **Grounding DINO over YOLO**: Prompt-driven zero-shot detection lets "delivery van" be a first-class label instead of shoehorning through COCO class IDs. Same approach as ViQA, so the home server runs one detection stack.
  **Reasoning**: Better delivery company detection was the user's explicit goal; GDINO handles open-vocabulary natively.

- **gemma3:4b over gemma4:31b**: For vehicle color/brand/delivery-logo ID, 4B is sufficient and fast. 31B is overkill and saturates ollama for other services.
  **Reasoning**: User specifically requested smaller Gemma. Can bump to `gemma3:12b` via env var if 4B accuracy falls short — no code change needed.

- **Two confidence gates**: `GDINO_BOX_THRESHOLD` (GDINO post-process cutoff, 0.35) + `MIN_CONFIDENCE` (act-on gate, 0.45). Split because GDINO sigmoid scores are not on the same scale as YOLO's.

- **`MODEL_PATH` kept as alias**: `main.py` log line references `config.MODEL_PATH`; kept as `MODEL_PATH = GDINO_MODEL_ID` so main.py needs no edits. Log reads `"YOLO >= 45% confidence | Model: IDEA-Research/grounding-dino-base"` — cosmetic, not a bug.

## Known Issues

- Log line still says "YOLO >= …" (cosmetic only — the literal string in `main.py:239`). Low severity, trivial fix if desired.
- `torch_dtype` deprecation warning from transformers: `[transformers] torch_dtype is deprecated! Use dtype instead!` — harmless, will go away when transformers API is updated in Dockerfile.

## Next Steps (Priority Order)

1. **Commit both repos** — root: `docker-compose.yml`; commander: 4 street-camera files
2. **Watch logs for first detection** — `docker logs -f street-camera` — confirm full pipeline works end-to-end
3. **Tune thresholds if needed** — if too many false positives: raise `GDINO_BOX_THRESHOLD`; if misses: lower it. Env-only change.
4. **GPU migration sweep** — move remaining services from `device_ids: ['0']` to `['1']`

## Files Actively Being Edited

- `docker-compose.yml` — GPU pinning fixed for `ollama-embed` + `street-camera`; gemma3/GDINO env vars added; HF cache mount added; `depends_on` swapped from `ollama-embed` to `ollama`
- `commander/projects/street-camera/config.py` — GDINO config replacing YOLO knobs; VLM repointed to `ollama:11434` + `gemma3:4b`
- `commander/projects/street-camera/detector.py` — YOLO replaced with Grounding DINO; `GDINO_LABEL_MAP` for free-text→canonical mapping; float bbox cast+clamp
- `commander/projects/street-camera/Dockerfile` — new `nvidia/cuda:12.8.0-devel-ubuntu24.04` base with cu130 torch + transformers
- `commander/projects/street-camera/requirements.txt` — added `numpy>=1.26`; dropped ultralytics (handled in Dockerfile)

## Context for Next Session

- **Plan file**: `/home/mello/.claude/plans/street-camera-gdino-refactor.md` — full design rationale, verification steps, and rollback procedure
- **Confidence scale**: GDINO sigmoid scores (0.0–1.0) trend lower than YOLO. 0.35 box threshold + 0.45 act-on are conservative starting points for street/driveway cameras. ViQA uses 0.18 for fine interior parts — street needs higher to reduce false positives.
- **`horse`/`sheep`/`cow` intentionally removed** from `ANIMAL_TYPES` (not in street prompt). To re-add: update `GDINO_PROMPT`, `ANIMAL_TYPES`, and `GDINO_LABEL_MAP` in lockstep.
- **ollama-embed still running** — `qwen3-embedding` model on it serves `memory-mcp`. Street-camera no longer depends on it.
- **GDINO weights location**: `/home/mello/.cache/street-camera-hf/` on host, mounted to `/root/.cache` in container
- **gemma3:4b location**: `/home/mello/.ollama/models/` (main ollama volume). `OLLAMA_KEEP_ALIVE=5m` so it unloads when idle.
- **VLM swap**: To try larger model: `docker exec ollama ollama pull gemma3:12b` then set `OLLAMA_VLM_MODEL=gemma3:12b` in compose and recreate container.

## Git State

- **Root repo** (`/home/mello`): branch `master`, last commit `9235acd "session handoff: hank local-ai rewrite"`, uncommitted: `docker-compose.yml`
- **Commander repo** (`/home/mello/commander`): branch `master`, uncommitted: `projects/street-camera/Dockerfile`, `config.py`, `detector.py`, `requirements.txt`
