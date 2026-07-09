---
name: LLM Inference Benchmark Plan (Ollama vs llama.cpp vs vLLM)
description: Three-backend tokens/sec comparison harness for Blackwell GPU: Qwen2.5-VL-7B, Nemotron-Cascade-2-30B, Nemotron-3-Super-120B. Plan from dual-GPU era — see GPU note
type: reference
---

# LLM Inference Benchmark Plan: Ollama vs llama.cpp vs vLLM

**Note**: plan was authored during dual-RTX-PRO-6000 era. GPU 1 was physically removed 2026-05-01 (see [[gpu-1-removed-2026-05-01-single-gpu-layout]]). Adjust GPU-pinning and the `tensor-parallel=2` bonus run accordingly — everything else still holds for the single 600W card.

## Model Lineup (Q4_K_M)

| Tier | Model (Ollama tag) | Arch | Size | Context | Notes |
|---|---|---|---|---|---|
| S | `qwen2.5vl:7b` | `qwen25vl` | 6.0 GB | 128k | VL model, text-mode benchmark |
| M | `nemotron-cascade-2:30b` | `nemotron_h_moe` | 24 GB | 262k | MoE, needs Ollama ≥0.17.1 |
| L | `nemotron-3-super:120b` | `nemotron_h_moe` | 86 GB | 262k | MoE, fits single 96GB at Q4 |

`nemotron_h_moe` arch support: llama.cpp mainline merged mid-2026; vLLM v0.10.x. **Phase 0 must verify both backends load the Nemotron tiers before downloads.**

## Backends — Native Format Per Backend (matches real deployment)

| Backend | Format | Install | Invocation |
|---|---|---|---|
| Ollama | native GGUF (already pulled) | already in Docker | `POST /api/generate stream:true`, parse `eval_count/eval_duration` |
| llama.cpp | same GGUF, symlinked from Ollama blobs | build from source w/ CUDA sm_120 | `llama-bench -m <gguf> -p 2048 -n 256 -b 1,8` + `llama-server` for streaming |
| vLLM | HF safetensors | `vllm/vllm-openai:latest` Docker image | `vllm bench latency/throughput/serving` |

**GGUF reuse trick**: Ollama's blobs at `/home/mello/.ollama/models/blobs/sha256-<hash>` are bit-identical GGUF. Symlink them into `/home/mello/llm-bench/gguf/<name>.gguf`. Zero redownload.

## Workload Matrix (greedy `temperature=0`, identical prompts)

| # | Workload | Prompt | Gen | Batch | Iters | Measures |
|---|---|---|---|---|---|---|
| 1 | Latency / decode | 512 | 256 | 1 | 5 | decode tok/s (chat UX) |
| 2 | Throughput / batched | 128 | 128 | 8 | 3 | total tok/s (server mode) |
| 3 | Prefill | 2048 | 32 | 1 | 5 | prefill tok/s + TTFT |
| 4 | Long-context | 8192 | 256 | 1 | 3 | decode tok/s @ long ctx |

One untimed warmup per (backend × model × workload). Report **median across iters** — robust to warmup artifacts.

## Layout

- Orchestrator: `/home/mello/commander/tools/llm_benchmark.py` (~400 lines, `BackendDriver` ABC + Ollama/LlamaCpp/Vllm impls + monitor subprocess copied from `gpu_stress_test.py`)
- GGUF symlinks: `/home/mello/llm-bench/gguf/`
- HF safetensors cache: `/home/mello/llm-bench/hf/` (per-model subdirs)
- llama.cpp source: `/home/mello/llama.cpp/` (built `build/bin/llama-{bench,cli,server}`)
- Outputs: `/home/mello/logs/llm-bench-<TS>/{monitor.csv, results.json, report.md, stdout/}`

## llama.cpp Build (Blackwell)

```bash
git clone https://github.com/ggerganov/llama.cpp /home/mello/llama.cpp
cd /home/mello/llama.cpp
cmake -B build -DGGML_CUDA=ON -DCMAKE_CUDA_ARCHITECTURES=120
cmake --build build -j
```

`-DCMAKE_CUDA_ARCHITECTURES=120` is the Blackwell sm_120 target.

## vLLM Invocation

```bash
docker run --rm --gpus '"device=0"' -p 8000:8000 \
  -v /home/mello/llm-bench/hf:/models \
  vllm/vllm-openai:latest --model /models/<name> \
  --dtype bfloat16 --max-model-len 16384 --gpu-memory-utilization 0.90
```

For 120B: try `--quantization fp8` or `--quantization awq`, fall back to BF16 if needed.

## Phases

| # | Phase | Time | Output |
|---|---|---|---|
| 0 | Compatibility & install gate (arch check, HF discovery, disk/VRAM preflight) | ~15 min | `compat.json` listing viable cells |
| 1 | Installs (llama.cpp build, vLLM pull, dirs) | ~20 min | |
| 2 | Model prep (GGUF symlinks + HF downloads w/ smoke loads) | ~30–60 min | |
| 3 | Build harness | ~1 hr | `llm_benchmark.py` |
| 4 | Dry run (1 backend × 1 model × all workloads, `--duration-multiplier 0.3`) | ~15 min | schema + bug-catch |
| 5 | Full matrix (3×3×4×iters ≈ 36 measured runs) | ~2–3 hr | |
| 6 | Report (env, compat matrix, 4 per-workload tables, VRAM/power, findings) | | `report.md` |

## Reasonableness Checks

- Ollama qwen2.5vl:7b decode should land 80–200 tok/s on Blackwell GPU at Q4 — if <20 or >500, investigate before trusting other rows.
- Any skipped cell must show `SKIPPED: <reason>` in the report — never silent.
- After Phase 5: GPU util <5% idle, no orphan llama-server/vllm/python processes.

## Out of Scope

- Multi-GPU tensor parallel for Ollama/llama.cpp (weak/no TP). vLLM `tensor-parallel=2` was a planned bonus run but is moot after GPU 1 removal.
- Quality evals (perplexity, MMLU) — throughput only.
- Streaming-specific metrics beyond TTFT.
- vLLM advanced features (speculative decoding, chunked prefill, prefix caching).
- CPU offload, mixed concurrent backend tests, model fine-tuning.

## Why This Matters (Context)

Following a PyTorch 2.9.1+cu128 matmul stress test on Blackwell that showed only ~15–30% of marketing-peak TFLOPS (cuBLAS sm_120 kernel maturity). Question shifted from "raw FLOPs" to "which inference runtime extracts the most real-world tok/s on this hardware?"
