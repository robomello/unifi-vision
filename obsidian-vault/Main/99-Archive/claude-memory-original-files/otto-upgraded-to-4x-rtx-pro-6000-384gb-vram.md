---
name: OTTO upgraded to 4x RTX PRO 6000 (384GB VRAM)
description: Work box (OTTO) now has 4x RTX PRO 6000 Blackwell 96GB = 384GB VRAM; the planned Threadripper+4x6000 upgrade is realized (confirmed 2026-06-19)
type: reference
---

The work box (OTTO, Mercedes) now has **4x RTX PRO 6000 Blackwell (96GB each) = 384GB total VRAM** (Roberto confirmed 2026-06-19: "at work I got 4x rtx 6000 pro"). This **realizes the planned Threadripper PRO 9985WX + 4x RTX PRO 6000 upgrade** and **supersedes** the "current: RTX 5090 32GB" line in the OTTO hardware note.

Implication: OTTO can now run the **largest open-weight coding LLMs locally** for the local-coder-pairs-with-Opus workflow, e.g. Qwen3-Coder-480B-A35B (4-bit ~240GB), GLM-4.6 (~355B MoE), DeepSeek-V3.x (tight at 4-bit), via vLLM/SGLang tensor-parallel across the 4 GPUs exposing an OpenAI-compatible endpoint (which otto-loop's ollama_runner / any /v1 client can target).

Keep distinct from the **home server** (separate machine): home = 1x RTX PRO 6000 96GB (GPU1, primary) + 1x RTX 5090 32GB (GPU0, secondary, PCIe x1). So model-size ceilings differ: ~96GB single-card at home vs 384GB at OTTO.
