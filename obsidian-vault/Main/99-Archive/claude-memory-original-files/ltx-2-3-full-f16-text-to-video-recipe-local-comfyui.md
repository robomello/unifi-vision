---
name: LTX 2.3 full-f16 text-to-video recipe (local ComfyUI)
description: How to generate LTX 2.3 full bf16 (dev, non-fp8) text-to-video locally: ComfyUI API route works, official ltx-pipelines blocked by missing HF Gemma dir
type: reference
---

Goal: local LTX 2.3 "full f16" = full bf16 DEV checkpoint (NOT fp8, NOT quantized) text-to-video.

WORKING ENGINE: ComfyUI API (http://localhost:8188, container "comfyui"). Confirmed 2026-06-05.
- Base the graph on ComfyUI/blueprints/"Text to Video (LTX-2.3).json". It is a single collapsed subgraph node; the real 46-node graph is in definitions.subgraphs[0]. The template DEFAULTS to fp8 + distilled lora, so it must be edited.
- Build a ~33-node API-format prompt from that subgraph. For PURE text-to-video (no input image): set bypass=True on both LTXVImgToVideoInplace nodes (ids 290 and 298) and feed EmptyImage black frames as their dummy image inputs. Inline all PrimitiveInt / ComfyMathExpression nodes as direct ints. Two-stage: stage 1 coarse 512x384 -> LTXVLatentUpsampler (x2 spatial) -> stage 2 refine 1024x768. POST /prompt, poll /history/{id}, download via /view.
- Models used (ALL local, NO fp8): checkpoint ComfyUI/models/checkpoints/ltx-2.3-22b-dev.safetensors (46GB full bf16); text encoder ComfyUI/models/text_encoders/gemma_3_12B_it.safetensors (full, not fp4); audio VAE from the same dev checkpoint; stage-2 refiner LoRA ltx-2.3-22b-distilled-lora-384.safetensors @ strength 0.5 (base stays full bf16); upscaler latent_upscale_models/ltx-2.3-spatial-upscaler-x2-1.1.safetensors.
- Perf: ~7 min (409s) on GPU 1 (CUDA_VISIBLE_DEVICES=1, 600W Workstation). Output 1024x768 (4:3, the blueprint native aspect), 121 frames (8x15+1) = 4.84s @ 25fps, h264 video + aac audio.

BLOCKED ENGINE: official Lightricks ltx-pipelines at /home/mello/LTX-2 (packages/ltx-pipelines, ti2vid_two_stages / ti2vid_one_stage). CLI in src/ltx_pipelines/utils/args.py. "full f16" there = simply do NOT pass --quantization (that flag forces fp8). BUT it requires --gemma-root pointing at an HF-format Gemma-3-12B-it directory (config.json + tokenizer + weights). Only the ComfyUI single-file gemma_3_12B_it.safetensors exists on disk, no HF dir, so Engine A is currently blocked. To unblock: place a real HF google/gemma-3-12b-it dir locally and pass --gemma-root, set HF_HUB_OFFLINE=1. Torch/CUDA for this Blackwell GPU works inside the comfyui container if the host uv env can't build CUDA torch.

Context: requested as a white-cat-talking-on-a-couch clip. Output kept at /data/sites/comfyui/output/ltx23_white_cat_couch_talking.mp4. comfyui_video.py (commander/tools) only wires WAN/Kandinsky, not LTX. See also commander/projects/ltx-dual-character and comfyui-workflows/ for other LTX graphs.
