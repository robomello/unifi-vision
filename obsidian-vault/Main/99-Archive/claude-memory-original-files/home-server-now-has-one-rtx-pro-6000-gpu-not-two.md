---
name: Home server now has ONE RTX PRO 6000 GPU (not two)
description: As of 2026-05-01, second GPU removed. Single 96GB GPU 0 only. device_ids:['1'] references are stale.
type: project
---

Roberto removed one of the two NVIDIA RTX PRO 6000 Blackwell 96GB GPUs from the home server as of 2026-05-01. Hardware now has ONE GPU only (96GB VRAM total, not 192GB).

**Why:** Physical hardware change. The previous dual-GPU setup (GPU 0 = 600W primary for ComfyUI/Whisper, GPU 1 = 300W secondary for n8n/ollama/factory-agent/commander/street-camera/casa-api) is no longer accurate.

**How to apply:**
- All ComfyUI, Whisper STT, and gen workloads now share the single remaining GPU 0.
- `device_ids: ['1']` references in docker-compose.yml are stale and will fail — anything pinned to GPU 1 must be re-pinned to GPU 0 or unpinned.
- VRAM contention is now real: ComfyUI + Ollama can no longer run heavy workloads simultaneously without eviction. `vram_guard.py` becomes more important, not less.
- No more parallel pipelines across two GPUs. Sequential only.
- Update `~/.claude/rules/context.md` Hardware section when next touched (currently still lists GPU 1).
