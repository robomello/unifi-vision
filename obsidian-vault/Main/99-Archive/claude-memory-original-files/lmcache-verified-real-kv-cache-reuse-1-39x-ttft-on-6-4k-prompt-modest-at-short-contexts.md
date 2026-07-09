---
name: LMCache verified: real KV-cache reuse, 1.39x TTFT on 6.4K prompt, modest at short contexts
description: Local test 2026-07-09: works as advertised but CPU-GPU transfer (0.35GB/s) offsets gains; wins grow with longer contexts/bigger models
type: reference
---

Tested https://github.com/LMCache/LMCache locally (2026-07-09), vLLM + Qwen2.5-7B, ~6.4K-token prompt, vLLM's native prefix caching DISABLED so the effect is LMCache alone:

- Run 1 (cold): `Inference Engine computed tokens: 0, LMCache hit tokens: 0` — stored ~7680 tokens of KV to CPU RAM in ~1.06s (chunks 0.1094-0.0820 GB).
- Run 2 (repeat): `LMCache hit tokens: 7680, need to load: 7680` — skipped prefill, retrieved 7680 tokens from CPU RAM in 1166ms (0.41GB @ 0.35GB/s).
- **TTFT: 1.702s cold -> 1.221s cached = 1.39x speedup.** Real cache hit, hard-proven from LMCache logs, not OS caching noise.

Verdict: works exactly as advertised, but 1.39x is modest — CPU<->GPU transfer partially offsets the compute saved. Wins grow with longer contexts, bigger models, or under GPU memory pressure (avoids OOM-driven eviction). Test was a synthetic repeated-paragraph prompt; disk/Redis tiers and PD disaggregation untested.

Housekeeping: container `lmcache-test` left running on GPU 0 (port 8010, ~11GB of the 32GB card) — tear down when done poking.

Related vLLM serving experiments: [Qwen3.6-27B NVFP4 vs Q8 coding test](qwen3-6-27b-nvfp4-vs-q8-coding-test-nvfp4-broken-on-vllm-nightly-2026-07-01.md).
