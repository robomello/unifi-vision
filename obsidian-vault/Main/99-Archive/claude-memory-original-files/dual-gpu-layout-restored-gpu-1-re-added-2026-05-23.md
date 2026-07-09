---
name: Dual-GPU layout restored — GPU 1 re-added 2026-05-23
description: Both RTX PRO 6000 Blackwell cards present again. GPU 0 (600W primary) + GPU 1 (300W Max-Q secondary). Supersedes all single-GPU memories from 2026-05-01.
type: project
---

GPU 1 was physically reinstalled on 2026-05-23. The home server is back to a dual-GPU layout. Verified 2026-05-24 via `nvidia-smi`: both cards visible, driver 595.58.03, CUDA 13.2.

**Current hardware (authoritative — per `~/.claude/rules/context.md`):**
- **GPU 0** — NVIDIA RTX PRO 6000 Blackwell Workstation Edition, 96GB, 600W TDP, bus `00000000:27:00.0`. Primary. Defaults for ComfyUI, Whisper STT, n8n, ollama, factory-agent, commander, street-camera, casa-api, viqa, claude-telegram, social-posting.
- **GPU 1** — NVIDIA RTX PRO 6000 Blackwell **Max-Q** Workstation Edition, 96GB, 300W TDP, bus `00000000:29:00.0`. Available again. **Workload allocation still TBD** — context.md has not yet assigned services to it.

**Why:** Hardware was reinstalled. The single-GPU period (2026-05-01 → 2026-05-23) is over.

**How to apply:**
- `device_ids: ['1']`, `cuda:1`, `CUDA_VISIBLE_DEVICES=1`, and `nvidia-smi -i 1` are **valid again**. They were silently failing during the single-GPU window — they work now.
- Don't auto-migrate workloads back to GPU 1 without checking with Roberto first. Allocation is "TBD" per context.md; if a service should move, ASK.
- `vram_guard.py` and `system-watcher.sh` still default to GPU 0 only (they were updated during the removal). If you want to monitor both, those scripts need explicit updates — flag to Roberto, don't change unilaterally.
- Session-start hook memory may still echo the stale "Single GPU only" line until the next consolidator/cron run picks up this entry. Trust `nvidia-smi` over a stale hook.

**Supersedes:**
- [[gpu-1-removed-2026-05-01-single-gpu-layout]] — single-GPU claim no longer true
- [[gpu-1-removed-temporary-2026-05-01]] — the "temporary" predicted in that note has resolved
- [[home-server-now-has-one-rtx-pro-6000-gpu-not-two]] — false as of 2026-05-23
- Service-assignment table in [[docker-gpu-config]] is partially stale — it lists pre-removal assignments where many services on `['1']` were migrated to `['0']` during the single-GPU window and have NOT been migrated back. Treat that table as historical until verified.

**Verification commands:**
```bash
nvidia-smi                              # host: should list both cards
docker exec comfyui nvidia-smi -L       # container view
cat /proc/driver/nvidia/version         # kernel module version
```
