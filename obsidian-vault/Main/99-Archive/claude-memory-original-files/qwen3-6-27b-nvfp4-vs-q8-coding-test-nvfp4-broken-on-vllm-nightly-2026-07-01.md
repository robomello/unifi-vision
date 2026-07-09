---
name: Qwen3.6-27B NVFP4 vs Q8 coding test: NVFP4 broken on vLLM nightly (2026-07-01)
description: NVFP4 quant numerically unstable on RTX PRO 6000 (52 tok/s but collapses); Q8 GGUF llama.cpp won 4/4 at 33.8 tok/s; FP8 KV cache is the crash culprit; ollama saturated by street-camera
type: project
---

Tested nvidia/Qwen3.6-27B-NVFP4 (2026-07-01) vs Q8_0 GGUF on real coding tasks (4 tasks, hidden test suites, code executed).

VERDICT: NVFP4 not production-ready on our stack. Q8 GGUF via llama.cpp won 4/4 vs 0-2/4.

Numbers: Q8_0 (bytkim MTP-pi-reasoning GGUF, llama.cpp server-cuda, GPU 1): 4/4 pass, stable 33.8 tok/s. NVFP4 (vLLM nightly, --quantization modelopt): ~52 tok/s when coherent (+54%) but intermittent numerical collapse — endless-thinking loops burning 16K tokens, and full degenerate output (8192 tokens of '!'). Symptoms match corruption in the hybrid linear-attention (GDN/mamba) path.

Stack gotchas learned:
- vLLM 0.20.1 (host venv) cannot load Qwen3.6 NVFP4 at all (weight shape mismatch). Needs vllm/vllm-openai:nightly.
- FP8 KV cache (vLLM auto-default) = instant CUDA illegal memory access or gibberish with this arch. Must use --kv-cache-dtype auto (bf16).
- CUDA graphs + low gpu-memory-utilization needs --max-num-seqs <= mamba cache blocks (error says the number).
- --enforce-eager works but drops 52 -> 8.7 tok/s (unusable).
- temp 0.2 makes official Qwen3.6 think forever; use temp 0.6 / top_p 0.95. Community MTP finetune tolerates 0.2.
- Production ollama (port 11434) has OLLAMA_NUM_PARALLEL=2, both slots permanently saturated by street-camera qwen2.5vl requests — external test requests queue forever. Use a dedicated container for benchmarking.
- Port 8767 on host is taken (uvicorn pid 10661).

Weights kept: /home/mello/models/Qwen3.6-27B-NVFP4 (22GB safetensors), /home/mello/models/Qwen3.6-27B-Q8-GGUF (29GB). Harness: /home/mello/models/qwen36_quant_coding_compare.py, outputs in qwen36-quant-compare-outputs/. Retest NVFP4 when vLLM ships a stable release with Qwen3.6 GDN fixes.

Also: the viral X claim ('NVIDIA smoked Unsloth, 26.3 vs 18.6 tok/s on DGX Spark') is unverified — numbers appear nowhere public; NVIDIA forum users actually report ~30 tok/s and complain it's slow.
