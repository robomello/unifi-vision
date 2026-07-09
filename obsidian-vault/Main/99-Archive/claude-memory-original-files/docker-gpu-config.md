---
name: Docker GPU Configuration
description: GPU device mapping for docker-compose services, dual RTX PRO 6000 Blackwell layout (GPU 0 is primary)
type: reference
originSessionId: <REDACTED-UUID-13>
---
# Docker GPU Configuration

## Hardware Map (Mello Home Server)

- GPU 0: NVIDIA RTX PRO 6000 Blackwell 96GB, 600W TDP — PRIMARY. ComfyUI default, Whisper STT.
- GPU 1: NVIDIA RTX PRO 6000 Blackwell 96GB, 300W TDP — secondary. n8n, ollama, factory-agent, commander, street-camera, casa-api. Available for parallel gen pipelines.

Both are 96GB Blackwell; GPU 0 has more headroom (600W) so it runs the primary workloads. GPU 1 is kept warm for parallel batch jobs.

## Current Assignments (2026-04-22)

| Service | device_ids | Notes |
|---------|-----------|-------|
| comfyui | `['0']` | Default primary image/video gen |
| whisper-stt | `['0']` | Shares GPU 0 with ComfyUI |
| claude-telegram (Joe) | `['0','1']` | Sees both GPUs |
| ollama-embed | `['0']` | Embeddings |
| n8n (x-n8n-deploy) | `['1']` | Anchor |
| factory-agent, commander, ollama, street-camera, casa-api | `['1']` | Secondary workloads |

## ComfyUI Binding

Default is GPU 0:

```yaml
comfyui:
  deploy:
    resources:
      reservations:
        devices:
          - driver: nvidia
            device_ids: ['0']
            capabilities: [gpu]
```

For parallel image/video pipelines that want both GPUs, the pattern is to run a **second** ComfyUI container (e.g. `comfyui2`) pinned to `device_ids: ['1']` on a separate port (e.g. 8189), and dispatch jobs round-robin. ComfyUI itself is single-process per GPU.

## Whisper STT

Pinned to GPU 0. Whisper load is steady and small (~3GB VRAM); plenty of headroom alongside ComfyUI.

## Why GPU 0 as Primary

- 600W TDP card has more sustained throughput than the 300W card
- Roberto's preference (2026-04-22): "gpu0 is better, default to it"
- Single-pipeline jobs run on GPU 0; multi-pipeline jobs fan out to GPU 1

## Verification

```bash
docker exec comfyui nvidia-smi -L       # should show the 600W card
docker exec claude-telegram nvidia-smi -L  # should show BOTH cards
nvidia-smi                               # host view
```

**How to apply:** New GPU-bound services default to GPU 0 unless they're part of the secondary stack (n8n, ollama, commander, factory-agent, street-camera, casa-api). For parallel batch pipelines, spin up per-GPU containers and dispatch — do not try to split a single ComfyUI process across devices.

## Updated: 2026-04-22
- ComfyUI flipped from GPU 1 -> GPU 0 (primary)
- claude-telegram (Joe) now sees both GPUs
- Secondary workloads stay on GPU 1
