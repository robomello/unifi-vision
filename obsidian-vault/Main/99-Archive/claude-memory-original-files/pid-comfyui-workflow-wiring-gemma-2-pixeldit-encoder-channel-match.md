---
name: PiD ComfyUI workflow wiring (Gemma-2 pixeldit encoder, channel match)
description: How to wire a working NVIDIA PiD super-res workflow in ComfyUI: gemma-2 pixeldit text encoder + base/variant channel matching
type: reference
---

NVIDIA PiD (Pixel Diffusion Decoder) super-res workflow wiring in ComfyUI (master/0.22). PiD is a PIXEL-space decoder (in_channels=3 RGB, patch 16) that upscales a base model's low-quality latent. See [ComfyUI pinned to master for PiD](#src-comfyui-pinned-to-master-for-pid-kronia-0-8-2-pin-audio-nan-patch) for the install side.

Required connections (all pieces already on the server as of 2026-05-30):
- **Text encoder (THE common gotcha):** PiD's `y_embedder` wants **2304-dim** conditioning = **Gemma-2 2B**. Use a `CLIPLoader`/`Load CLIP` with **clip_name=`gemma-2-2b-it_elm.safetensors`** (in models/text_encoders/) and **type=`pixeldit`**. ComfyUI recipe string confirms: "pixeldit: gemma 2 2B elm". A CLIP-L/Z-Image encoder gives 768-dim → `RuntimeError: mat1 and mat2 ... (Nx768 and 2304x1536)`. Both positive AND negative CLIP Text Encode must use this pixeldit CLIP.
- **Base ↔ variant channel match:** PiD flux variant = 16-ch latent (Flux1-dev OR Z-Image, which reuse Flux1's 16-ch VAE); PiD flux2 variant = 128-ch latent (Flux2-dev). Mismatch → `ValueError: Input latent has 16 channels, this model variant expects 128`.
- **PiDConditioning node:** latent_format=`flux` (auto-detects Flux1 vs Flux2 by channel dim), degrade_sigma=0 for a clean latent. Attaches lq_latent+degrade_sigma to the positive conditioning.
- **Chain:** CLIPLoader(gemma pixeldit)→CLIP Text Encode(pos/neg); base model→low-res 16ch latent→PiDConditioning(positive, latent); Load Diffusion Model(PiD _flux_ .pth)→model; SamplerCustom(model, pos=PiDConditioning out, neg) → PiD outputs PIXELS directly (no separate VAE decode of PiD output). Distilled 4-step = LCM sampler, cfg≈1.
- VAE for encoding the base latent: flux2-vae.safetensors (Flux2) or ae.safetensors (Flux1/Z-Image).
