---
name: Joel LoRA bootstrap — compact plan (no local gen)
description: Roberto provides ChatGPT-generated Joel images; we face-lock to Qwen anchor, cull, train.
type: project
---

**Compact plan as of 2026-05-11.** Joel LoRA bootstrap dropped the local 60-image generation step — Roberto is providing ChatGPT-generated Joel images instead.

| step | what | who |
|---|---|---|
| 1 | Drop ChatGPT-generated Joel images into `.state/training_sets/joel/raw/` (Telegram bot upload or filesystem) | Roberto |
| 2 | *(optional)* Face-swap each against `joel_qwen2512.png` using `Face Swap PixelSmile Workflow.json` → save to `face_locked/` | Claude/bot |
| 3 | Cull keepers → move to `curated/` | Roberto (or Claude with veto) |
| 4 | Train Joel LoRA in `ai-toolkit` on `curated/` against Qwen Image 2512 base | Claude/bot |
| 5 | Repeat for Cintia + Claudio once their anchors are picked | both, later |

**Why:** ChatGPT Image's identity preservation is good enough that we don't need to bootstrap with local Qwen 2512 generations. Skipping that step saves ~30 min of GPU lock and lets Roberto control the diversity directly (he picks the prompts in ChatGPT). The face-swap pass is the cheap insurance that all training images are pegged to the Qwen anchor's exact face — without it, Roberto's ChatGPT Joels may drift subtly from the locked anchor.

**How to apply:**
- **Bucket layout** (per-vlogger, same for Cintia/Claudio later):
  - `training_sets/<vlogger>/raw/` — source uploads (ChatGPT outputs, references, etc.)
  - `training_sets/<vlogger>/face_locked/` — after the face-swap-to-anchor pass
  - `training_sets/<vlogger>/curated/` — what actually trains the LoRA
- **Upload paths**: Telegram (caption = `joel|cintia|claudio` routes; default joel/raw), filesystem at `.state/training_sets/<v>/raw/`, viewer at `https://franchise.synai.ai/training_sets/<v>/raw/`
- **Anchor**: `bible/vloggers.json` → joel.canonical_hero_ref = `.state/hero_refs/joel/joel_qwen2512.png`
- Don't run step 4 (LoRA training) without confirming step 3 has at least 25–30 strong, varied keepers — too few and the LoRA overfits, too narrow and Joel can only be drawn from the trained angles
