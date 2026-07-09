---
name: Unsloth LLM Fine-Tuning
description: Unsloth installed for local LLM fine-tuning, venv location, GPU mapping, and next steps for Mercedes manual training
type: project
originSessionId: <REDACTED-UUID-37>
---
Unsloth 2026.4.4 installed on 2026-04-09 for local LLM fine-tuning.

**Why:** Roberto wants to fine-tune models on Mercedes W138 technical manuals (service docs, operating procedures) to build a domain-specific assistant.

**How to apply:** When resuming this work, activate the venv and use the correct GPU.

## Setup
- Venv: `~/.venvs/unsloth` (system-site-packages, inherits PyTorch 2.9.1+cu128)
- Activate: `source ~/.venvs/unsloth/bin/activate`
- GPU mapping: `CUDA_VISIBLE_DEVICES=0` = RTX PRO 6000 96GB, `CUDA_VISIBLE_DEVICES=1` = RTX 3080 Ti 12GB
- Flash Attention 2 not working, falls back to Xformers (no perf impact)

## Verified Working
- Model loading (Qwen3 0.6B 4-bit)
- LoRA adapter attachment
- SFTTrainer training (5 steps completed, loss 3.2 -> 1.9)
- Adapter saving to disk

## Recommended Model
- Qwen2.5-Coder 32B for coding tasks (~20GB in 4-bit, fits easily on 96GB GPU)
- Unsloth ID: `unsloth/Qwen2.5-Coder-32B-Instruct-unsloth-bnb-4bit`

## Next Steps
1. Get Mercedes manuals in digital format (PDF/Word)
2. Extract text, chunk into sections
3. Generate Q&A pairs from chunks (use Claude CLI)
4. Fine-tune Qwen2.5-Coder 32B or similar on the pairs
5. Export to GGUF for Ollama serving
