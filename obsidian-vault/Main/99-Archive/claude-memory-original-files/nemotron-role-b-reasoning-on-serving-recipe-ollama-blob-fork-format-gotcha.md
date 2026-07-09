---
name: Nemotron Role-B reasoning-ON serving recipe + Ollama-blob fork-format gotcha
description: How to serve Nemotron-3-Super-120B reasoning-ON for the Opus-planner-replacement eval; the Ollama GGUF won't load upstream
type: project
---

Project: ~/commander/projects/nemotron-coding-eval (Role B = test local Nemotron reasoning-ON as an Opus-4.6 PLANNER replacement). Roberto picked Role B on 2026-06-13.

GOTCHA (cost hours): the Ollama `nemotron-3-super:120b` blob (`~/.ollama/.../sha256-0fc53cc…`, and the symlink `~/llm-bench/gguf/nemotron-3-super-120b.gguf`) is a FORK-format GGUF — HF-style tensor names (`mtp.layers.N.mixer.experts.K.down_proj`, `ffn_latent_in/out`, `exp_probs_b`), 1803 tensors, NO `moe_latent_size` key. NO upstream llama.cpp version loads it (latest server-cuda13 fails on tensor count/shape; Apr-21 clone uses `ffn_latent_down/up`). Ollama runs it but CANNOT cap thinking (think:true/false only) → hard tasks run away (a07 = 30k+ think tokens, 0 answer). So Ollama is useless for reasoning-ON.

FIX (validated 2026-06-13): download the CLEAN upstream GGUF `unsloth/NVIDIA-Nemotron-3-Super-120B-A12B-GGUF:UD-Q4_K_M` (3 shards ~82.5GB; bartowski equivalent is fallback). Serve on `ghcr.io/ggml-org/llama.cpp:server-cuda13` (Blackwell sm_120 native): `-ngl 999 -c 32768 --jinja --reasoning-format deepseek --reasoning-budget 8192 --temp 0 --seed 42`. The --reasoning-budget forces </think> at the cap → model answers; temp=0 → n=1 deterministic. De-risk gate a07: finish=stop, real code, ~87s (was infinite in Ollama). Mount the GGUF's DIR (split shards), point -m at the 00001 shard.

STATUS: serving + harness fully built/validated on home (driver llama_server, stats.py McNemar/bootstrap, 4-stratum loader, opus-high via `claude --effort high`). 300-task stratified run + taskgen are handed to baby-otto (GPUs left 2026-06-14). Everything in `baby-otto-kit/` (cc_llama_reason.sh, RUNBOOK §6, de-risk-gate.json) and plan `~/.claude/plans/nemotron-roleB-planner-eval.md`.
