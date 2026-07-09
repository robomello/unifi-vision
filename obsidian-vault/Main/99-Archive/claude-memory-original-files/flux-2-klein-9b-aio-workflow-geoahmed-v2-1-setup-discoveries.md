---
name: FLUX 2 Klein 9B AIO Workflow (geoahmed v2.1) — Setup & Discoveries
description: Required models, custom nodes, and non-obvious sampling discoveries for the FLUX.2 Klein 9B Ultimate 6-in-1 ComfyUI workflow
type: reference
---

**Source**: civitai.com/models/2543188 (author: geoahmed / Ahmed Lahmidi). Workflow JSON at `/home/mello/comfyui-workflows/flux2_klein_ultimate_v2.1.json` (122 nodes, 19 groups: F1=txt2img, F2=KV-edit, F3=face+pose, F4=inpaint, F5=blend, plus refiner / upscaler / Florence2 auto-mask / 4 ControlNet preprocessors / NAG / color match).

**Why**: The non-obvious denoise / encoder rules below cause silent quality failures (artifacts, plastic skin, matrix shape errors) that aren't visible from the workflow JSON alone — worth keeping out-of-band.

**How to apply**: Open the workflow in ComfyUI, then check this note for any setup issue.

## Required assets (all present in `comfyui` container as of 2026-05-01)

| Asset | Container path | Source |
|---|---|---|
| `flux-2-klein-9b.safetensors` (17G) | `/app/models/diffusion_models/` | already present |
| `flux-2-klein-9b-kv.safetensors` (17G) — KV variant for ReferenceLatent edits | `/app/models/diffusion_models/` | already present |
| `qwen_3_8b.safetensors` (16G) — text encoder, type=`flux2` | `/app/models/clip/` (or text_encoders) | already present |
| `flux2-vae.safetensors` (321M) | `/app/models/vae/` | already present |
| `klein_9b_enhancer_v2.safetensors` (663M) — **mandatory**, strength 0.7, LAST in LoRA chain | `/app/models/loras/Flux2Klein/` | huggingface.co/reverentelusarca/detail-enhancer-flux-klein-9b (downloaded 2026-05-01) |
| `V2_flux_klein_4.safetensors` (optional LoRA slot) | not installed | preset filename in workflow; replace with any Klein-compatible LoRA or set strength=0 |
| `flux-2-klein-9b-Q8_0.gguf` (8GB-VRAM path only) | not needed on Roberto's 96GB GPU | Klein GGUF on HF if ever required |

## Required custom nodes (all installed)

`rgthree-comfy` (Fast Groups Bypasser) · `ComfyUI-Florence2` (auto-mask) · `ComfyUI-GGUF` (UnetLoaderGGUF) · `comfyui_controlnet_aux` (LineArt/HED/Tile/DepthAnythingV2) · `ComfyUI_essentials` (ImageScaleBy etc.) · `sd-perturbed-attention` (NormalizedAttentionGuidance — installed 2026-05-01 from github.com/pamparamm/sd-perturbed-attention).

## Non-obvious sampling rules (read before changing anything)

1. **4 steps, CFG=1, sampler=euler, scheduler=simple** — Klein 9B is 4-step distilled. Higher steps don't improve quality. CFG>1 breaks the output.
2. **Encoder must match base model size**: Klein 9B → Qwen 3 8B encoder (`type=flux2`); Klein 4B → Qwen 3 4B. Mixing causes silent matrix-shape errors.
3. **Refiner denoise sweet spot = 0.85**. Below 0.85 with `EmptyLatentImage` produces severe artifacts because 4-step distilled sampling can't correct corrupted random-noise structure. Use `VAEEncode` of an actual image as latent input if you want denoise <0.85.
4. **`ReferenceLatent` (F2 KV-edit) operates via KV attention, NOT latent blending** — denoise is effectively 1.0 regardless. The model always generates fresh, guided by the reference. This is fundamentally different from img2img.
5. **Faces must be upright** — Klein cannot process rotated or upside-down face references in F3.
6. **Enhancer LoRA must be LAST in the LoRA chain** at strength 0.7. Detaching it forces re-wiring every group's output. It fixes Klein's flat-plastic skin and washed-out colors.
7. **Klein over-saturates reds**. Append `"histogram equalization, white balance correction, color grade"` to prompts, or use the built-in Color Correction node after the refiner.
8. **Only one F-group active at a time** (F1–F4) to save VRAM. Refiner + upscaler can stay on alongside.

## Pipeline cheat sheet
- **F1 txt2img**: prompt → KSampler → SaveImage `F2K_txt2img`
- **F2 KV-edit**: ref image + edit instruction → KV-conditioning. Example: "Replace the red dress with a navy blazer. Keep pose, expression, background unchanged."
- **F3 face + pose**: face ref (upright portrait) + pose ref (DAZ render) → multi-ReferenceLatent → composed scene
- **F4 inpaint**: mask manually OR enable Florence2 group ("Segment the shirt"). Denoise 0.5–0.8 for changes, 0.3–0.5 for tweaks.
- **Refiner**: any image → ReferenceLatent + KSampler, denoise 0.85
- **Upscaler**: 4× UltraSharp, then `ImageScaleBy 0.5` for net 2× (toggle to 1.0 for final)

## Prompt style
Describe like a photograph, not SD-style: *"A 30-year-old man in a navy overcoat standing on a rain-soaked Prague street at dusk, tungsten streetlights casting warm shadows, shot on Canon R5 85mm f/1.4, clean digital file, histogram equalization"*.

## Known gaps
- F4 inpainting is imperfect on complex shapes — paint rough colors in the mask first to guide it; nudge denoise in small steps.
- Civitai download for this workflow requires `?token=$CIVITAI_API_TOKEN` query param (header auth or aria2 redirect-following fails with 403 on the B2 redirect — use `curl -fL`).
