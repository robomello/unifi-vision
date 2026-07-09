---
name: Docker compose: explicit COMFYUI_API_URL override per service
description: Always set COMFYUI_API_URL=http://comfyui:8188 in each service's environment: block; .env alone leaks host-side localhost into containers.
type: feedback
---

When wiring a new Docker service to ComfyUI, ALWAYS set `COMFYUI_API_URL: http://comfyui:8188` explicitly in the service `environment:` block of docker-compose.yml. Do NOT rely on the host `.env` file alone — `.env` carries the host-side value (`http://localhost:8188`, used by non-containerized scripts), and `env_file:` loads it into the container where `localhost` is the container itself, so ComfyUI calls fail with `All connection attempts failed`.

**Why:** On 2026-05-03 Joe (claude-telegram) silently lost ComfyUI access for image OCR/QwenVL because it relied only on `env_file: ./.env`. Sister services (image-telegram, dreamvault-gen, casa-api, avatar-pipeline, skool-api, ai-psychologist) all already had the explicit override. Joe did not. Roots: rules/context.md already says "Docker hostname: ALWAYS `comfyui:8188`, NEVER `localhost:8188`".

**How to apply:** Any new compose service that imports `comfyui_describe.py`, makes ComfyUI HTTP calls, or runs the local-image-gen path must explicitly set `COMFYUI_API_URL: http://comfyui:8188` in its `environment:` block. Audit by running `awk '/^  [a-z]/{svc=$1} /COMFYUI_API_URL/{print svc, $0}' docker-compose.yml` and cross-checking against any service that imports comfy code.
