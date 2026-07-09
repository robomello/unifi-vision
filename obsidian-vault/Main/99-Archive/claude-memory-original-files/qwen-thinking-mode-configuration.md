---
name: Qwen Thinking Mode Configuration
description: How to disable thinking/reasoning on Qwen3/Qwen3.5 across vLLM, Ollama, llama.cpp. Recreated from lost source. Key: think=False, --reasoning-parser none, /no_think tag.
type: reference
---

## Qwen Thinking/Reasoning Configuration (RECREATED — original lost)

**Status:** Original source file was lost during memory migration. Recreated from context.

### What It Was
Reference document about disabling the thinking/reasoning feature on Qwen models (Qwen3, Qwen3.5) across different inference backends.

### Key Facts (reconstructed from server context)

**vLLM:**
- Qwen3 reasoning parser at: /home/mello/models/vllm-venv/lib/python3.12/site-packages/vllm/reasoning/qwen3_reasoning_parser.py
- Disable thinking: pass --reasoning-parser none or set enable_thinking=False in generation params
- vLLM serving: use --enable-auto-tool-choice without --reasoning-parser to skip thinking output

**Ollama:**
- Qwen3 models support /no_think tag in prompts to disable reasoning
- Or set think=False in API params
- Used in GSPOC project: options.think=False for qwen3.5:35b-a3b

**llama.cpp:**
- Thinking tokens appear inside <think>...</think> tags
- Strip via post-processing or use --no-thinking flag if available

**ComfyUI (Qwen Image 2512, QwenVL):**
- Text encoders don't expose thinking mode (image models, not reasoning)
- AILab_QwenVL node caps max_tokens at 2048

**CodeForge Arena benchmarks:**
- Qwen3-Coder and Qwen3.5 variants tested with and without thinking
- Thinking mode adds latency but improves complex reasoning scores

### How to Apply
When running Qwen models for fast inference (not reasoning tasks), disable thinking to save tokens and latency. For GSPOC inspection: think=False. For CodeForge benchmarks: test both modes.

Why: Original qwen-thinking.md was lost during memory migration. Recreated from server context and project references.

How to apply: When configuring Qwen model serving or running benchmarks, reference this for thinking-mode toggle across backends.
