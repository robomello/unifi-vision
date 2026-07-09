---
name: DSpark speculative decoding: 2.5x winner, vLLM-only, maps to OTTO port 8001 slot
description: DSpark draft ~2.5x on Qwen3-14B in local bench; Ollama can't run it; deploy target is OTTO's empty vLLM slot at 8001
type: reference
---

From tech review of https://youtu.be/yvAHJZAf1xM (session 2026-07-08). Local benchmarks (bench.py harness, DeepSpec/vLLM stack) on Qwen3-14B target:

- `deepseek-ai/dspark_qwen3_14b_block7` — winner, ~2.5x speedup
- `deepseek-ai/dflash_qwen3_14b_block7` — 2nd, ~2.3x
- `deepseek-ai/eagle3_qwen3_14b_ttt7` — 3rd, ~1.5x
- Target model: `Qwen/Qwen3-14B` (~28 GB)

**Key gotcha: Ollama cannot run this.** Speculative decoding with a separate draft checkpoint needs the DeepSpec/vLLM serving stack. OTTO's `qwen3:14b` is a plain Ollama Q4_K_M — not a swap-in.

**Deployment mapping:** OTTO already has an empty vLLM slot reserved at port 8001 for "a 14B reasoning model" (was pending Nemotron-Cascade-14B). Same pattern as `DASD-4B-Thinking` already on vLLM at port 8000. DSpark+Qwen3-14B is a candidate for that slot.

See [OTTO upgraded to 4x RTX PRO 6000](otto-upgraded-to-4x-rtx-pro-6000-384gb-vram.md) and [LLM inference benchmark plan](llm-inference-benchmark-plan-ollama-vs-llama-cpp-vs-vllm.md).
