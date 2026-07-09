---
name: ComfyUI Model Behavior
description: Which ComfyUI models produce which visual styles -- Qwen Image is smooth/digital, Z-Image is painterly, critical for art style matching
type: reference
---

## Model Style Characteristics (tested 2026-03-28)

### Qwen Image 2512
- Produces **smooth, detailed, photorealistic-leaning** images
- Even with "oil painting" in prompt, output looks digital/illustrative
- The Lightning LoRA makes it even smoother (speed optimization)
- Without Lightning LoRA + CFG 5.0: slightly more textured but still smooth
- Best for: photorealistic scenes, detailed compositions, portraits
- NOT good for: traditional art textures, visible brushstrokes, painterly look

### Z-Image Full (bf16)
- Produces **painterly, textured** output with visible brushstrokes
- Actually looks like oil painting when prompted for it
- 25 steps, CFG 4.0, res_multistep sampler, qwen_3_4b encoder, ae.safetensors VAE
- Note: may add fake artist signatures -- use negative prompt "no signature, no text"
- Best for: oil paintings, traditional art styles, Etsy wall art
- Re-downloaded on 2026-03-28 after drive migration deleted it

### Flux 2 Dev (fp8 mixed)
- 34GB model, needs mistral_3_small_flux2_bf16 encoder + flux2-vae
- Re-downloading on 2026-03-28
- Known for: high quality, good prompt following

## Key Lesson
Match the model to the desired art style. Don't try to force Qwen Image into painterly output -- use Z-Image instead.
