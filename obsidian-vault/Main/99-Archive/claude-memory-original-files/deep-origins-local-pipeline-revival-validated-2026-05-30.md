---
name: Deep Origins local pipeline revival (validated 2026-05-30)
description: Deep Origins evolution-video pipeline validated fully local: GPT Image 2 keyframes + local Wan 2.1 FLF2V morph + ffmpeg + YouTube @EvolutionLab; the cost fork is resolved (morphs run local = free)
type: project
---

Deep Origins (animal "evolution" timelapse videos; container `deep-origins` :8060; site videos.evolutionlabs.blog; YouTube @EvolutionLab) was built, shipped ~9 episodes Feb-Mar 2026, then abandoned at the local-vs-cloud fork. Revived and validated end-to-end 2026-05-30.

WHY IT STALLED: not failure (people love it). Roberto quit because the manual grind got monotonous. Classic automation candidate. And PLAN.md's #1 open item was "[DECIDE] local vs cloud for image/morph/eval."

VALIDATED ARCHITECTURE (all local except trivial keyframe credits):
- Research -> species + prompts: existing 9-step pipeline works. Artifacts: /data/sites/deep-origins/jobs/<id>/research/*.json. Saber-tooth job = 8b538692 (good prompt source).
- Keyframes: GPT Image 2 via MyDesigns best on prompt-adherence/anatomy (beat local Qwen 2512, Nano Banana Pro). Local Qwen 2512 also strong but drifts (gave Smilodon a lion mane); needs art-directed prompts, not the thin stored image_prompt (which is just short_description).
- Morph (the brick old version paid Kling for): LOCAL Wan 2.1 FLF2V proven. 720x1280, 49 frames, 20 steps euler/simple cfg6 ~= 9.5 min / 3.1s clip on RTX 6000. Free.
- Assembly: deep_origins/tools/ffmpeg_tools.py already complete + local.
- Publish: youtube-uploader (valid token, upload scope, @EvolutionLab) already wired.

KEY INSIGHT: the expensive cloud cost was ALWAYS the morphs (Kling ~$0.25 x ~17/episode), not images. So GPT Image 2 keyframes (~3 credits) + LOCAL Wan morphs = best look AND ~free. Resolves the fork.

TECH GOTCHAS (cost real time):
- MyDesigns gpt-image-2 (`--engine gpt2`, tool /home/mello/commander/tools/mydesigns_dream.py): ratios ONLY 2:3 / 1:1 / 3:2. 9:16 -> empty HTTP 500 (looks like an outage but is a bad-ratio reject).
- Wan 2.1 flf2v_720p_14B is NOT resolution-flexible: must be native 720x1280 or "tensor a vs b at dim 2".
- clip_vision_h.safetensors = 1152 (SigLIP), WRONG for Wan (needs ViT-H 1280 = clip_vision_vit_h.safetensors). FLF2V also works fine with clip-vision OMITTED (endpoints lock from VAE start/end frames).
- Working Wan FLF2V graph: UNETLoader(wan2.1_flf2v_720p_14B_fp16) + CLIPLoader(umt5_xxl_fp16,type=wan) + VAELoader(wan_2.1_vae) + ImageScale->720x1280 + WanFirstLastFrameToVideo(start/end_image) + ModelSamplingSD3(shift8) + KSampler(euler,simple,cfg6,20steps) + VAEDecode + SaveImage -> ffmpeg h264.
- Roberto also has an "LTX 2.3 Transition Studio" + FLF blueprints, but they are opaque subgraph nodes (awkward headless); LTX-transition is an alternative morph path to try for speed/quality.

ASSETS: test scripts /home/mello/do_localtest/ (gen.py = Qwen image, wan_morph.py = morph). Outputs + 4-way keyframe comparison + morph mp4 at /data/sites/evolution/_localtest/ (served videos.evolutionlabs.blog/_localtest/).

REMAINING: (1) integrate gpt-image keyframes + Wan morph into deep_origins, replacing tools/fal_tools.py (Flux/Kling) and tools/gemini_tools.py; (2) autopilot: animal queue + n8n/cron schedule + one-tap Telegram approve so episodes ship without him.
