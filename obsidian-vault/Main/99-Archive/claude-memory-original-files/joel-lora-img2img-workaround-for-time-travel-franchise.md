---
name: Joel LoRA img2img workaround for time-travel-franchise
description: Joel LoRA v1 is identity-undertrained; use img2img with raw reference + LoRA 0.8 + denoise 0.55 until retrain
type: project
---

Joel LoRA v1 (Qwen Image, rank 32, 1500 steps, 52 images) is identity-undertrained for the time-travel-franchise project — produces consistent but off-target face when used standalone.

Working pipeline for Joel-faced gens until LoRA is retrained:
- **img2img** with a raw reference photo as init latent (e.g. `training_sets/joel/raw/joel_20260512_130251_762f048b.jpg`)
- VAEEncode the reference → KSampler latent_image
- LoRA strength: **0.8** (lower to avoid overriding the locked face)
- Denoise: **0.55** (balance — face stays, scene flexes)
- Steps 25, CFG 3.0, euler, simple scheduler (training-matched)
- Skip the pipeline's force-stacked Lightning 4-step LoRA — it washes identity

Why: Standalone LoRA learned an average of 52 curated AI-gen training images that had drifted from the canonical reference. img2img bypasses this by seeding the latent with the actual reference face.

How to apply: Use this for any time-travel-franchise hero shots (Joel/Cintia/Claudio) until LoRAs are retrained at higher rank with face-locked crops. Full helper builder: see Joel i2i v5 in conversation history.

Long-term fix: retrain at rank 64+ using `raw/` + `expression_refs/joel_facs_grid.jpg` cropped + `hero_refs/` instead of `curated/` AI-gen images.
