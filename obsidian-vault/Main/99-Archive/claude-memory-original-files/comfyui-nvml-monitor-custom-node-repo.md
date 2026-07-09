---
name: ComfyUI-NVML-Monitor (custom node + repo)
description: Multi-GPU NVML telemetry chip for ComfyUI; lives at /home/mello/ComfyUI/custom_nodes/ComfyUI-NVML-Monitor and at github.com/robomello/ComfyUI-NVML-Monitor
type: project
---

**Repo:** https://github.com/robomello/ComfyUI-NVML-Monitor (main branch)
**Local path:** `/home/mello/ComfyUI/custom_nodes/ComfyUI-NVML-Monitor/`
**What it is:** ComfyUI custom node that adds a draggable telemetry chip (always visible in the ComfyUI tab) plus a click-to-expand popup with two tabs (GPU, System). NVIDIA-only via `pynvml`. Polls `/nvml_monitor/stats` every 1.5s.

**Structure:**
- `monitor.py` — backend collector. Already enumerates ALL GPUs via `nvmlDeviceGetCount()`; returns `gpus[]` in the JSON.
- `__init__.py` — registers `WEB_DIRECTORY = "./web"` and the `/nvml_monitor/stats` aiohttp route on `PromptServer`.
- `web/nvml_monitor.js` — vanilla JS frontend. Chip + popup. Position/open-state persisted in localStorage (`nvml_monitor.pos`, `nvml_monitor.popup_open`).
- `screenshot/` — `chip.jpg`, `chip-multi-gpu.png`, `popup-gpu-tab.png`, `popup-system-tab.png`.

**Multi-GPU support (added 2026-05-24):**
1. Chip now renders every GPU labeled `G0`/`G1`/... and badge shows `NVIDIA ×N`. Single-GPU layout unchanged. (commit `36878fc`)
2. README + screenshots updated. (commits `9810af5`, `72af16a`)
3. **Docker-compose change (NOT in repo, local only):** ComfyUI service in `/home/mello/docker-compose.yml` widened from `device_ids: ['0']` to `device_ids: ['0', '1']` plus `CUDA_VISIBLE_DEVICES: "0,1"`. Without this, NVML inside the container only sees GPU 0 regardless of code. ComfyUI still defaults to cuda:0 — exposing GPU 1 doesn't force any workload onto it.

**Color thresholds in chip/popup:** util/VRAM green<60, yellow 60-85, red >=85. Temp green<65°C, yellow 65-82, red >=82. Power green<70% of limit, yellow 70-90, red >=90.

**Useful behavior:** Popup GPU tab shows an "External (other containers / host)" row when in-container VRAM accounting doesn't match the NVML total — surfaces VRAM held by sibling containers (ollama, etc.).

**To rebuild after compose changes:** `docker stop comfyui && docker rm comfyui && docker compose up -d comfyui` (per home server rule — `docker restart` does not pick up compose changes).
