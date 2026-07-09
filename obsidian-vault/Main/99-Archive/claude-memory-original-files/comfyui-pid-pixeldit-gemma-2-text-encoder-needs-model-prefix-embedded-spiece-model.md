---
name: ComfyUI PiD/pixeldit Gemma-2 text encoder: needs model. prefix + embedded spiece_model
description: Bare-key gemma-2 safetensors silently loads as CLIP-L 768 in ComfyUI pixeldit/lumina2; fix = re-key with model. prefix + embed spiece_model byte tensor
type: reference
---

PiD (NVIDIA pixel-space SR decoder) and Lumina2 use a Gemma-2 2B text encoder via `CLIPLoader type=pixeldit`. The conditioning must be **2304-dim** (PiD `y_embedder.proj` = nn.Linear(2304, 1536)).

**Failure mode (silent):** A raw HF-export gemma-2 safetensors with BARE keys (`embed_tokens.weight`, `layers.N.*`, `norm.weight`) is NOT detected by ComfyUI. `comfy/sd.py detect_te_model()` identifies Gemma-2 only by `'model.layers.0.post_feedforward_layernorm.weight'` (note the `model.` prefix). With bare keys it returns None, `clip_type=pixeldit` is ignored, and ComfyUI builds a default **CLIP-L (768-dim, SD1ClipModel)** with NO weights loaded. There is NO load error — it only blows up later at sampling with a cryptic `mat1 and mat2 shapes cannot be multiplied (300x768 and 2304x1536)` (300 = `_PIXELDIT_MAX_LENGTH`, 768 = CLIP-L hidden).

**Second requirement:** the pixeldit/lumina2 tokenizer (`Gemma2BTokenizer` -> `SPieceTokenizer`) reads the SentencePiece model from a byte tensor stored IN the safetensors under key `spiece_model`. Without it: `ValueError("invalid tokenizer")`. Must be the Gemma-2 256k-vocab tokenizer (piece 107 = `<end_of_turn>`), NOT Gemma-3's 262144 one.

**Fix recipe (what I did, verified working):**
1. Re-key: prepend `model.` to every weight key. `tensors["model."+k] = f.get_tensor(k)`.
2. Embed tokenizer: `tensors["spiece_model"] = torch.frombuffer(bytearray(open(tok,'rb').read()), dtype=torch.uint8).clone()`. Source of the correct Gemma-2 256k tokenizer.model: `ComfyUI/custom_nodes/ComfyUI-PiD/comfyui_pid/tokenizer/tokenizer.model` (vocab 256000, piece107=`<end_of_turn>`).
3. `save_file(tensors, dst, metadata={"format":"pt"})`.

Output file: `models/text_encoders/gemma-2-2b-2304-pixeldit.safetensors`. Verified: loads as `PixelDiTTE_` / `Gemma2_2B`, cond shape `(1, 300, 2304)`. Original broken file `gemma-2-2b-it_elm.safetensors` kept (unused).

Workflow `z_image_turbo_to_pid_03` (CLIPLoader node 74) repointed to the fixed file; ran end-to-end SUCCESS (Z-Image 16ch latent -> PiD `_flux_` 16ch variant -> 4096x4096 pixel-space decode). Also note: PiD `_flux_` variant = 16ch latent (Z-Image/Flux1), `_flux2_` = 128ch — must match the base model's VAE latent channels.

Supersedes the earlier (incorrect) note that said to just point the CLIPLoader at `gemma-2-2b-it_elm.safetensors` with type pixeldit — that file's bare keys make it silently load as CLIP-L.
