---
name: Deep Origins — Prompts in NocoDB + Opus 4.6 Image Prompt Generator
description: Deep Origins research pipeline: 7 prompts editable in NocoDB via prompts_loader.py with 60s TTL + hardcoded fallback; step_09b image-prompt generator pinned to claude-opus-4-6 (not opus alias) to match n8n baseline
type: project
---

# Deep Origins — Prompts in NocoDB + Image Prompt Model Pin

Deep Origins (`origins.synai.ai`) is a FastAPI app at `/home/mello/deep-origins/` generating evolutionary timeline videos from species names. 10-step research pipeline → Opus synthesizes per-species `short_description` → ComfyUI (Qwen Image 2512).

## Prompts in NocoDB (DONE)

All 8 research prompts moved from Python constants to NocoDB so Roberto can iterate without code changes.

**Base**: `pjf6dzz40r87uqh` (existing Deep Origins base) — keep project locality.
**Table**: `deep_origins_prompts`

Schema (mirrors `fruit_battle_prompts` + `Variables` CSV addition):
| Column | Type |
|---|---|
| Name (Single line text, unique) | slug, e.g. `resolve_genus` |
| Body (Long text) | template w/ `{var}` placeholders |
| Description (Single line text) | UI label |
| Variables (Single line text) | informational CSV of placeholder names |
| Active (Checkbox) | only one row per Name should be active |
| Version (Number) | increment on edit |
| UpdatedAt (DateTime) | |

Rows seeded (all Active=true, Version=1): `resolve_genus`, `perplexity_research`, `validate_claude`, `validate_gemini_system`, `validate_gemini_user`, `generate_lineage_system`, `generate_lineage_user`.

**Key Python gotcha**: `{{...}}` double-brace patterns inside prompt bodies (JSON schema examples) must be preserved verbatim. Python `str.format()` treats them as escaped literal braces — round-trips unchanged.

## prompts_loader.py (the only new abstraction)

`deep_origins/tools/research/prompts_loader.py` (~80 lines):
- `await load_prompt(name, **format_kwargs)` — fetches active row, applies `.format()`, returns string
- 60 s per-name TTL cache (`_cache: dict[str, tuple[str, float]]`, `asyncio.Lock`)
- On NocoDB failure or no active row → fallback to hardcoded constant in `prompts.py`, log WARNING (drift visible)
- New NocoDB client method: `get_active_prompt_from(table, name)` — generic version of `get_active_prompt` that takes table as parameter (the original hardcodes `fruit_battle_prompts`)

**Important**: `prompts.py` was NOT deleted — it remains the fallback source. The 5 step files (`step_01_resolve`, `step_05_perplexity`, `step_06_validate`, `step_07_validate_gemini`, `step_08_generate`) mechanically swap `CONSTANT.format(...)` for `await load_prompt("slug", ...)`.

## Step 9b Image-Prompt Generator: Pinned to claude-opus-4-6

**File**: `deep_origins/tools/research/step_09b_image_prompts.py:119`

Changed `model="sonnet"` → `model="claude-opus-4-6"`. Sonnet produced image prompts whose resulting images were below the n8n baseline (which uses `claude-opus-4-6`).

Direct comparison on Acanthostega gunnari:

| Aspect | Opus 4.5 (`claude-opus-4-5-20251101`) | Opus 4.6 (`claude-opus-4-6`) |
|---|---|---|
| Gill anatomy | wrote "external gill slits" — factually wrong | "internal gill arches visible as slit openings" |
| Period flora | Lepidodendron + Calamites (anachronistic — those are Carboniferous, Acanthostega is Late Devonian) | Archaeopteris, Rhacophyton, Prototaxites, charophyte algae |
| Pose specificity | "stalking small prey" | "gripping submerged Archaeopteris root tangles to hold position in slow current" |
| Lateral line | not mentioned | "lateral line grooves running along the body" |
| Composition | basic 9:16 | split water-level shot, frame between above/below water surface |

**Why `claude-opus-4-6` not the `opus` alias**: the alias resolves to whatever the CLI considers current Opus (4.7). Roberto's n8n baseline was 4.6 and we want behavior to match that reference flow. Explicit version is also reproducible.

`run_claude` (`_claude_cli.py:71-91`) passes `model` straight through as `--model <value>`. `_PER_SPECIES_TIMEOUT = 180` and `_PARALLEL = 3` unchanged — Opus 4.6 is slower than Sonnet but well under 180 s at this prompt size.

## Deploy Pattern (NOT `docker restart`)

```bash
docker stop deep-origins
docker rm deep-origins
docker compose up -d deep-origins
docker logs --tail 30 deep-origins
```

`docker restart` does NOT reload Python modules — must remove + recreate. Documented home-server gotcha.

## Out of Scope (Explicitly)

- Re-running step_09b across already-generated jobs: the per-species **↻ Regen prompt** button on the species view lets Roberto upgrade prompts on demand.
- Tuning `_flatten_prompt_json` paragraph builder. Revisit only if image quality still off after model bump.
- Richer structured-JSON image prompt (n8n-style: `scene/subjects/color_palette/lighting/camera/effects`). Current 10-word `short_description` is the present format; richer is a separate feature.
- Frontend prompt editing in `origins.synai.ai` — Roberto edits in NocoDB UI (`nocodb.synai.ai`).
- Per-animal prompt overrides — single template per name only.
- Cache-bust endpoint — 60 s TTL is enough; restart for immediate pickup.
