---
name: GPU 1 removed 2026-05-01 — single-GPU layout
description: GPU 1 physically removed; only GPU 0 (RTX PRO 6000 Blackwell 96GB) remains. All device_ids:['1'] migrated to device_ids:['0'].
type: project
---

GPU 1 was physically removed from the home server on 2026-05-01.
The system now has a single GPU: GPU 0 (NVIDIA RTX PRO 6000 Blackwell 96GB, 600W TDP).

**Why:** Hardware reduction. All workloads now share GPU 0.

**How to apply:**
- Never use `device_ids: ['1']`, `cuda:1`, or `CUDA_VISIBLE_DEVICES=1`. They will silently fail Docker container creation (exit 128) and cause `nvidia-smi -i 1` to error.
- Anything that previously ran on GPU 1 now runs on GPU 0: n8n-main, n8n-worker-1/2/3, ollama, factory-agent, commander, street-camera, claude-telegram, viqa, social-posting, casa-api, fish-speech, ai-toolkit.
- The `system-watcher.sh` script and `vram_guard.py` were updated to query GPU 0 (`-i 0`, `VRAM_GUARD_GPU_INDEX=0`).
- If a self-healing recovery loop fires repeatedly with "Cannot determine GPU memory" or "insufficient GPU memory (-1MB free)", check for any new code/config that hardcoded GPU 1 again.

**Files updated on the migration day:**
- `/home/mello/docker-compose.yml` (n8n anchor + 9 service blocks)
- `/home/mello/fish-speech/compose.base.yml`
- `/home/mello/ai-toolkit/docker-compose.yml`
- `/home/mello/system-watcher.sh` (5 hardcoded `-i 1` calls + device-node check + VRAM alert text)
- `/home/mello/commander/tools/vram_guard.py` (default `VRAM_GUARD_GPU_INDEX` 1 → 0)
- `/home/mello/.claude/rules/context.md` (Hardware section)
