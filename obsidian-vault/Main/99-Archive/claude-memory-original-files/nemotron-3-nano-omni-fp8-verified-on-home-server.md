---
name: Nemotron-3-Nano-Omni FP8 verified on home server
description: Working vLLM recipe + results for NVIDIA Nemotron-3-Nano-Omni-30B-A3B-Reasoning FP8 (all 4 modalities) on RTX Pro 6000
type: reference
---

Tested nvidia/Nemotron-3-Nano-Omni-30B-A3B-Reasoning on 2026-06-03. Mamba2-Transformer hybrid MoE, 31B total / ~3B active, omni input (video+audio+image+text) -> text only, 256k ctx, English only. Components: Nemotron 3 Nano LLM + CRADIO v4-H vision encoder + Parakeet tdt-0.6b-v2 speech encoder. License: NVIDIA Open Model Agreement, ungated.

FP8 variant (33GB, NVIDIA's recommended precision FOR the RTX Pro 6000) runs on ONE RTX Pro 6000 96GB via Docker image vllm/vllm-openai:v0.20.0. Footprint ~89GB VRAM at --max-model-len 131072 with --kv-cache-dtype fp8. Weights load in 25s. BF16 variant is 62GB (also fits 96GB); NVFP4 is 21GB.

Launch flags that worked (vLLM 0.20.0): --trust-remote-code --reasoning-parser nemotron_v3 --enable-auto-tool-choice --tool-call-parser qwen3_coder --video-pruning-rate 0.5 --allowed-local-media-path / --media-io-kwargs '{"video":{"fps":2,"num_frames":256}}'. For audio/video, pip install librosa soundfile inside the container (base image lacks them). Use --gpus '"device=1"' to stay off ComfyUI's GPU.

All 4 modalities verified: text reasoning (bat-and-ball = $0.05, correct), image (grid-of-dots geometry accurate), ASR (Parakeet, near-perfect transcription, 2.8s), video (256-frame temporal multi-scene description, 6.8s).

GOTCHA: ~/.local/bin/hf and huggingface-cli are BROKEN (shebang points to nonexistent /usr/local/bin/python3.11). Download via: python3 -c "from huggingface_hub import snapshot_download; snapshot_download('<repo>')" (hf_xet is installed, accelerates automatically). Do NOT set HF_HUB_ENABLE_HF_TRANSFER=1 (hf_transfer not installed).

Test harness + media at ~/nemotron-test/ (run_tests.py, launch.sh, media/). Caveat: fp8 kv-cache uncalibrated (q/k scale 1.0) -> minor accuracy; drop --kv-cache-dtype fp8 for BF16 KV given VRAM headroom.
