---
name: LongCat-Video-Avatar-1.5 install + patches
description: Working audio-driven avatar video gen on RTX PRO 6000 Blackwell (sm_120). Path: /home/mello/commander/projects/longcat-video
type: project
---

# LongCat-Video-Avatar-1.5 — Working install

**Location**: `/home/mello/commander/projects/longcat-video/`
**Status**: Working as of 2026-05-22. Produces 832x480 25fps MP4 from portrait + audio.
**License**: Repo MIT, but **model weights are academic-only — no commercial use** (no Etsy/POD/TikTok).

## Why: stock install doesn't work on this box
Repo pins torch 2.6+cu124 + flash-attn 2.7.4; that combo doesn't compile sm_120 kernels and OOMs the 62 GB system RAM during model loading. Required 5 patches to make it run on a single RTX PRO 6000 Blackwell.

## How to apply: re-run command
```bash
cd /home/mello/commander/projects/longcat-video
.venv/bin/torchrun --nproc_per_node=1 run_demo_avatar_single_audio_to_video.py \
  --context_parallel_size=1 \
  --checkpoint_dir=./weights/LongCat-Video-Avatar-1.5 \
  --stage_1=at2v \
  --input_json=assets/avatar/single_example_1.json \
  --use_distill --model_type avatar-v1.5 --use_int8
```
Output: `outputs_avatar_single/at2v_demo_1.mp4`

## Environment
- Python 3.12 venv at `.venv/` (uv-created)
- torch 2.11.0+cu128 (native sm_120, NOT the pinned 2.6+cu124 from requirements)
- flash-attn NOT installed (sm_120 incompatible with 2.7.4)
- xformers NOT installed
- onnxruntime CPU only (separator runs on CPU; install `onnxruntime-gpu` to fix)
- `constraints.txt` locks torch/torchvision/torchaudio to cu128 so future `uv pip install` doesn't clobber to PyPI cu124

## Selective HF download (saved ~52 GB vs full)
Use `huggingface_hub.snapshot_download` with `ignore_patterns` — CLI `--ignore-patterns` is NOT a flag, only the Python API supports it.
- Avatar-1.5 repo: skip `base_model/diffusion_pytorch_model-*.safetensors`, `whisper-large-v3/flax_model.msgpack`, `whisper-large-v3/pytorch_model*`, `whisper-large-v3/model.fp32*`, `assets/*.mp4`. Result: ~21 GB.
- Base LongCat-Video repo: only `tokenizer/**`, `scheduler/**`, `vae/**`, `text_encoder/**` (skip the 30+ GB `dit/`). Result: ~22 GB.
- Total: 43 GB on disk.

## The 5 patches (do NOT lose these on `git pull`)
1. `weights/LongCat-Video-Avatar-1.5/base_model_int8/config.json`: set `"enable_flashattn2": false`
2. `run_demo_avatar_single_audio_to_video.py` (~line 113): text_encoder load gets `device_map="cuda:0", low_cpu_mem_usage=True`; vae gets `low_cpu_mem_usage=True` + `.to(local_rank)`; dit gets `.to(local_rank)` immediately after lora; MEM prints added.
3. `longcat_video/modules/quantization.py` `load_quantized_dit`: instantiate model + QuantizedLinears inside `with torch.device("meta"):` (zero bytes); call `model.load_state_dict(state_dict, strict=True, assign=True)`; `del state_dict; gc.collect()`. This avoids the ~54 GB fp32 nn.Linear allocation peak that OOM-killed us.
4. `longcat_video/modules/avatar/attention.py`: add `import torch.nn.functional as F`; replace `raise RuntimeError("Unsupported attention operations.")` with `x = F.scaled_dot_product_attention(q, k, v, scale=self.scale)`.
5. `longcat_video/modules/attention.py`: same SDPA fallback for self-attn; for the variable-length cross-attn, loop per batch item — `q_chunks = q[0].split([N]*B, dim=0)` and `k_chunks = k[0].split(kv_seqlen, dim=0)`, call SDPA per chunk, concat back.

## Memory profile (after patches)
- text_encoder: 1.1 GB RSS, 10.6 GB VRAM (device_map loads direct to GPU)
- VAE: 1.2 GB RSS, 10.8 GB VRAM
- DIT loaded (CPU): **1.3 GB RSS** (meta+assign trick — was OOM-killing at 54 GB before)
- DIT moved to CUDA: 3.4 GB RSS, 25.8 GB VRAM
- Inference peak VRAM: ~25-30 GB (plenty of headroom on 96 GB card)

## Pitfalls hit
- `--ignore-patterns` is not a `huggingface-cli download` flag (Python API only)
- `uv pip install -r requirements.txt` with `--extra-index-url cu128` causes torch version conflicts (cu128-index packages pin torch ranges) — install torch separately, then deps from PyPI only
- PyPI torch overwrites cu128 torch unless you reinstall the cu128 wheel after deps (or use constraints.txt)
- `device_map="cuda:0"` for text_encoder DOES work (verified RSS=0.8 GB for solo load) — the OOMs were caused by the DIT fp32 allocation peak, not the text encoder
- `onnxruntime==1.16.3` from requirements_avatar.txt has no cp312 wheels — bumped to `>=1.17.0`
- Removed from requirements (Roberto's rules / sm_120 incompat): `flash-attn`, `openai`, `libsndfile1` (system pkg), `tritonserverclient` (wrong PyPI name), `cffi` pin

## Next steps if extending
- Install `onnxruntime-gpu` to move vocal separator off CPU (current 37s separation is CPU-bound)
- Build a [[avatar-agent]]-style wrapper around the run script for programmatic invocation
- Test multi-audio inference: `run_demo_avatar_multi_audio_to_video.py` (same patches likely apply)
- Watch for git pull conflicts on the 3 patched source files
