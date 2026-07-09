---
name: qwen3-vl vLLM backend decommissioned
description: qwen3-vl (Qwen3-VL-32B vLLM vision API for hank receipt OCR) fully removed 2026-06-05: container + 22.9GB image + compose block deleted; model weights kept
type: project
---

On 2026-06-05 the qwen3-vl service was fully decommissioned at user request.

What it was: vLLM (vllm/vllm-openai:v0.20.0) serving Qwen3-VL-32B-Instruct as an OpenAI-compatible vision API for hank receipt OCR. Internal endpoint http://qwen3-vl:8000/v1 (host 127.0.0.1:8064), pinned to GPU 1 (600W Workstation, device_ids ['1']), gpu-memory-utilization 0.92 (~90GB).

What was removed: the stopped container (docker rm), the 22.9GB vllm/vllm-openai:v0.20.0 image (docker rmi, disk reclaimed), and the entire service block from /home/mello/docker-compose.yml. It had already been behind the "disabled" compose profile + restart:"no" since 2026-06-04. docker-compose.yml now has 70 services and validates as YAML.

What was kept: model weights at /home/mello/ComfyUI/models/LLM/Qwen-VL/Qwen3-VL-32B-Instruct (left intact because ComfyUI QwenVL vision may share them).

Context that triggered this: after a GPU 0 (Max-Q, bus 27) driver hang, the box was power-cycled. qwen3-vl did not auto-start (restart:"no"); user chose to remove it entirely rather than bring it back.

Side note found during cleanup: /data/projects/hankbook/hank/.env line 6 is malformed (key contains a space), which makes `docker compose config` / `docker compose up` fail when it reads hank's env_file. The already-running hank container is unaffected.
