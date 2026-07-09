---
name: Image generation banned sources
description: Never use fal.ai or kie.ai for IMAGE generation; local ComfyUI + MyDesigns only. Video is unaffected.
type: feedback
---

For ANY image generation: use local ComfyUI (Flux 2 Dev, Qwen Image 2512, Z-Image Turbo, Flux 2 Klein) and/or MyDesigns Dream AI (gpt2 = ChatGPT Image 2, nano-banana-pro, etc). NEVER fal.ai for images. NEVER kie.ai for images.

Why: Roberto stated 2026-05-10 'do not make images with fal.ai or kie.ai'. Local models are the default; MyDesigns is the cloud comparison.

How to apply: Image generation in /home/mello/commander/projects/time-travel-franchise (and broadly) routes through:
- /home/mello/skills/local-image-gen/scripts/generate_image_local.py --model {qwen2512,flux,klein,turbo}
- /home/mello/commander/tools/mydesigns_dream.py --engine {gpt2,nano-pro,flux-2-max,...}

When comparing styles for hero refs, generate the SAME prompt across multiple local models + ChatGPT Image 2 (gpt2 engine on MyDesigns) and let Roberto pick. Note: fal.ai is still allowed for VIDEO (HappyHorse character consistency), and kie.ai is still allowed for VIDEO (Veo3, Kling). Only IMAGE gen on those services is banned.
