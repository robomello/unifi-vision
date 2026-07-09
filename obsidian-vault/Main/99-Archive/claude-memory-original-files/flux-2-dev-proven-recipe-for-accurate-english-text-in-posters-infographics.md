---
name: Flux 2 Dev: proven recipe for accurate English text in posters/infographics
description: Verified 2026-05-03: Flux 2 Dev fp8 + per-panel structured prompt + 1024x1536 yields 100% correct English titles in 8-panel infographics. Qwen 2512 fails ~30% of multi-word titles.
type: project
---

# Flux 2 Dev — Proven Text-Rendering Recipe (verified 2026-05-03)

**Goal:** generate multi-panel infographics where every English title is rendered correctly (no garbled letters, no missing letters, no swapped words).

**Tested on:** 8-panel yoga tutorial poster (2x4 grid, anime ink wash style, character + pose + title + bullet text per panel).

## Winner
- **Model:** `flux2_dev_fp8mixed.safetensors` (Flux 2 Dev fp8)
- **Encoder:** Mistral 3 Small (handles short uppercase labels reliably)
- **Resolution:** **1024x1536** (going to 1280x1920 broke the numbering — duplicate "2"s and "8"s)
- **Steps:** 30
- **CFG:** 1.0 (Flux default — do not raise)
- **Seed:** 42 worked first-shot
- **VRAM:** ~12 GB (fits with VLLM running, unlike Qwen 2512 which needs ~38 GB)

## Prompt structure (mandatory)
Use **explicit per-panel breakdown** with this template:

```
Panel <ordinal> number <N> title <SHORT TITLE>, <pose description>.
```

Example that worked: `Panel one number 1 title MOUNTAIN POSE, anime woman standing tall arms at sides.`

## Title rules (critical)
- **Single word or two short words MAX** (≤12 chars total)
- **AVOID** long compound words: DOWNWARD, ALIGNMENT, FOUNDATION (consistently breaks)
- **PREFER:** DOG POSE over DOWNWARD DOG; WARRIOR TWO over WARRIOR II (Roman numerals fail); CHILD POSE over CHILD'S POSE (apostrophes drop letters)
- All caps reinforces text accuracy

## Failure modes seen during testing
| Model | Failure |
|---|---|
| Qwen Image 2512 BF16 (30 steps) | Headers ~62% correct: DOWNWRD instead of DOWNWARD, LOW L NGE, WARRIOR III instead of II |
| Flux 2 Dev @ 1280x1920 | Text spelling perfect, but numbering broken: panels duplicated, 3/5/6 skipped |
| Flux 2 Dev with full sentence titles | Drops random letters in last 2 panels |

## Reproduction command
```
COMFYUI_URL=http://localhost:8188 python3 /home/mello/skills/local-image-gen/scripts/generate_image_local.py \
  "<prompt with explicit per-panel structure>" \
  --model flux --width 1024 --height 1536 --steps 30 --seed 42
```

## When to use Qwen 2512 instead
- Single hero image with 1-2 lines of long text
- Body bullet-text where you can post-overlay correct strings via PIL
- Photorealistic posters where Flux's flatter style hurts

## Reference test artifact
`/data/sites/comfyui/output/yoga_02e_flux2dev_v3.png` — 8-panel yoga poster, all 8 titles + 8 numbers correct first try.
