---
name: Joel LoRA v2 — img2img Batch Generation Settings (locked)
description: 70-image seed set for Joel LoRA v2 retrain — MyDesigns Dream AI GPT Image 2 img2img, quality=high, ratio=2:3, parallel=2, locked settings
type: project
---

# Joel LoRA v2 — img2img Batch Generation

**Goal**: 70 reference images of Joel (35 prompts × 2 samples) via MyDesigns Dream AI img2img using GPT Image 2 → seed set for v2 LoRA training. v1 was identity-undertrained — see [[joel-lora-img2img-workaround-for-time-travel-franchise]].

## Inputs

- **Prompts**: `/home/mello/commander/projects/time-travel-franchise/.state/training_sets/joel/_chatgpt_prompts_v2.md` — 35 prompts in 5 buckets (F=face×10, H=half-body×6, P=physique×10, C=clothed×4, A=angle×5)
- **Reference image** (img2img source): `/home/mello/commander/projects/time-travel-franchise/.state/training_sets/joel/selected/joel.jpg`
- **Output dir**: `/home/mello/commander/projects/time-travel-franchise/.state/training_sets/joel/raw/`
- **Runner**: `/tmp/joel_lora_v2_batch.py` (self-contained, idempotent)

## Locked Settings (DO NOT CHANGE without asking Roberto)

| Setting | Value | Reason |
|---|---|---|
| Engine | `gpt-image-2` (alias `gpt2`) | Roberto's directive 2026-05-13 — only GPT Image 2 for edits |
| Mode | `GPT_IMAGE_1_EDIT` (auto from `edit()`) | Verified working w/ `engineId=gpt-image-2` |
| Quality | `high` | Roberto chose `high` over `medium` 2026-05-13 |
| Ratio | `2:3` (1024×1536) | Vertical/person-centric prompts |
| Samples per call | `2` | 2 variations per prompt |
| Image strength | `50` | Balanced — keeps face, allows scene change |
| Magic prompt | OFF (`magic_prompt=False`) | Prompts already detailed |
| Output filename | `joel_<bucketLetter>_<promptID>_s<N>_<uuid8>.png` | e.g. `joel_F_F1_s1_e43c07f5.png` |
| Parallelism | 2 concurrent workers | Roberto's "send 2 at a time" |

## Cost / Runtime

- 35 prompts × 2 samples = 70 images
- Quality `high`: 6–15 credits/image expected (420–1050 credits total). First test (1 image) didn't decrement cached balance of 1475 — confirm with `python3 /home/mello/commander/tools/mydesigns_dream.py --credits` pre-flight.
- ~150 s per call at quality high; samples=2 similar or slightly longer.
- Wall clock at parallel=2: ~17–25 min for all 35 calls.

## Idempotency

Runner skips prompts that already have ≥2 output files matching `joel_<bucket>_<promptID>_*.png` in `raw/`. Safe to re-run on interrupt.

## Post-Batch

1. Verify count: `ls .../joel/raw/joel_*.png | wc -l` ≥ 70
2. Open franchise-curator UI: `https://franchise.synai.ai/curate/joel`
3. Reject bad outputs (face drift, unwanted body hair, etc.) via the ✕ Reject button
4. Caption + ai-toolkit retrain — see v1 notes in [[joel-canonical-anchor-locked-qwen-image-2512]]

## Deferred Questions

- Whether `the same man` in prompts should become `the man in the attached reference image`. Test image's face matched exactly, so current phrasing works. If face drifts during batch, switch phrasing.
- Telegram bot routing for finished images — non-blocking; raw/ feeds the curator review.
