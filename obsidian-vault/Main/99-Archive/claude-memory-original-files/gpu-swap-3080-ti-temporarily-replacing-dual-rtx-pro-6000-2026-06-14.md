---
name: GPU swap: 3080 Ti temporarily replacing dual RTX PRO 6000 (2026-06-14)
description: 12GB 3080 Ti in place of dual RTX PRO 6000; heavy GPU services stopped/pinned; restore via ~/restore-gpu-services.sh
type: project
---

On 2026-06-14 both RTX PRO 6000 Blackwell cards (96GB each) were physically removed and a single RTX GeForce 3080 Ti (12GB, now NVML index 0) installed temporarily.

Problem found: system-watcher.service was in an active restart loop (50,699+ "Restarting" attempts logged) trying to revive comfyui/ollama/claude-telegram, which can't start on 12GB. That churn was thrashing the box.

Stabilization done (all REVERSIBLE):
- system-watcher.sh: commented out ollama, claude-telegram, comfyui from the CONTAINERS watch list (marked `GPU-SWAP-DISABLED 2026-06-14`). Backup: ~/commander/system-watcher.sh.gpu-swap-bak. Watcher still guards postgres/cloudflared/disk/DNS.
- Set restart=no and stopped: comfyui, ollama, ollama-embed, street-camera, claude-telegram, ai-toolkit.
- Left RUNNING (fit in 12GB, healthy): whisper-stt (~2.3GB), viqa (~1.1GB), tts-service, plus all non-GPU infra (commander, n8n, nocodb, surrealdb, cloudflared, web frontends).

RESTORE when the big GPUs are back: run `bash ~/restore-gpu-services.sh` (restores watcher list from backup, sets restart=unless-stopped, starts the 6 containers, restarts the watcher).
