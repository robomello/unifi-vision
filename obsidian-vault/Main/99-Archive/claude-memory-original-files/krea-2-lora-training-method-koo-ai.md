---
name: Krea 2 LoRA Training Method (KoO Ai)
description: Dataset-first workflow for training realistic Krea 2 LoRAs; detailers/upscalers hurt a well-trained LoRA
type: reference
---

Source: KoO Ai YouTube "Stop Using Detailers! Here is How to Train Perfect Krea 2 LoRAs" (2026-07-02, https://youtu.be/MduUJay3_OY). Full analysis: /home/mello/commander/projects/youtube-analyses/2026-07-02_koo-ai_stop-using-detailers-train-perfect-krea-2-loras.md

Core thesis: dataset quality/variety dominates every hyperparameter. If the dataset is good, base Krea 2 already carries fine detail (skin, hair, environment coherence) — running a detailer OR upscaler (e.g. Nvidia PID) on the output DEGRADES it, does not improve it. That's the title's whole argument.

Dataset spec (from on-screen KoO.Ai infographic, more precise than his narration):
- Target 24-40 base images. Rule: 70-80% clean base shots + 20-30% targeted extra shots.
- Base split: 30% front-facing close-ups, 20% medium close-ups, 15% three-quarter, 10% side profile, 10% full body, 10% natural poses/expressions, 5% close details (skin/eyes/hair).
- Include well-visible FULL-BODY shots — a face-only dataset breaks on full-body prompts.
- Extras (+2-3 each, repeat a consistent prompt phrase): golden hour, blue hour/night, gym/fitness, mirror selfie, specific makeup, studio flash, side face, ultra-detailed skin close-up.
- Generate dataset with ChatGPT image gen (his pick; more identity-consistent than Nano Banana Pro, which drifted). Source reference face on Pinterest ("aesthetic girl"). 1-2 bad images can ruin a LoRA — be strict.

Training (RunPod + Ostris AI Toolkit UI template):
- Train on Krea 2 RAW (not Turbo/tool). GPU: RTX PRO 6000 (Krea raw is heavy).
- Steps ~3,000-3,500 max; save every ~250 steps, keep ~10 checkpoints, TEST THEM ALL (best checkpoint varies per scene).
- Learning rate 0.02 (barely matters), batch size default, resolution 1024. Skip/delete in-training sample images (don't reflect ComfyUI output).
- Trigger word = nonsense token (e.g. Electra / 4zzur4) so it won't collide with base-model concepts. Auto-caption then hand-edit: swap subject noun for trigger, inject concept tags.
- RunPod storage is ephemeral: DOWNLOAD checkpoints, TERMINATE pod after (it bills continuously).

ComfyUI usage: keep sampler on res multi-step; LoRA strength sweet spot 0.85-1.0 (lower if too rigid to follow style prompts).

Caveat: his step numbers are inconsistent (calls 1,750 both undertrained and "very good"; ships a 00007500 checkpoint) — trust "keep all checkpoints and test," not any single number.
