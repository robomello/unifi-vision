---
name: ComfyUI PiD flux2 super-res wiring (Flux 2 base -> PiD)
description: Flux2(128ch)->PiD needs flux2 PiD variant + flux2-vae; PiDConditioning latent_format only flux|sd3 (Flux1/2 auto-detected by channel dim)
type: reference
---

Built `flux2_to_pid_01.json` (Flux 2 Dev base -> PiD super-res), verified end-to-end.

Key gotchas building a PiD super-res chain on a Flux 2 base:
- **PiDConditioning `latent_format` only accepts `flux` or `sd3`** (NOT `flux2`). Flux1 (16ch) vs Flux2 (128ch) is **auto-detected from the latent channel dim**. So keep `latent_format=flux` for BOTH Flux1 and Flux2 bases; sd3 is the only manual override. Setting "flux2" -> `value_not_in_list` validation error.
- Channel match is enforced by the **PiD MODEL variant**, not latent_format: `PiD_*_flux_*` = 16ch (Z-Image/Flux1, VAE `ae.safetensors`), `PiD_*_flux2_*` = 128ch (Flux 2, VAE `flux2-vae.safetensors`). Feed the base sampler's LATENT straight into PiDConditioning.latent.
- Flux 2 Dev t2i base nodes: `UNETLoader(flux2_dev_fp8mixed)` -> `BasicGuider` (no ModelSampling node needed); `CLIPLoader(mistral_3_small_flux2_bf16, type=flux2)` -> `CLIPTextEncode` -> `FluxGuidance(4)` -> BasicGuider; `EmptyFlux2LatentImage` (128ch); `RandomNoise`+`KSamplerSelect(euler)`+`Flux2Scheduler(20)` -> `SamplerCustomAdvanced`; decode preview with `flux2-vae`.
- PiD stage unchanged from the flux version except model variant: `SamplerCustom` (cfg 1, add_noise) + `KSamplerSelect(lcm)` + `BasicScheduler(simple,4)` + `EmptyChromaRadianceLatentImage` canvas + `VAELoader(pixel_space)` decode.
- res2kto4k variant = ~4x upscale; verified 960x544 base -> 3840x2176 (arbitrary sizes OK, not just 1024->4096).
- The pixeldit gemma encoder is the re-keyed `gemma-2-2b-2304-pixeldit.safetensors` (see [[comfyui-pid-pixeldit-gemma-2-text-encoder-needs-model-prefix-embedded-spiece-model]]).

Verifying ComfyUI workflows headlessly: pull a graph from `GET /history`, patch node inputs, `POST /prompt` (API format = {id:{class_type,inputs}}), poll `/history/<id>` for execution_error vs status_str=success. Build UI workflows by cloning real nodes from a working workflow (valid slot structures) and rewiring links, rather than synthesizing litegraph JSON from scratch.
