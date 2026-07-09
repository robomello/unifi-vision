---
name: Workflow files are source of truth — never hand-translate to Python builders
description: All ComfyUI/video pipelines must file-load workflows + inject runtime params. UI->API conversion is fine. Discuss before editing any workflow.
type: feedback
---

For ALL ComfyUI image and video pipelines (Origins, Mug Pipeline, Fruit Battle, Frozen Survival, Deep Origins phase 2, LTX-2, Kling, VEO, HappyHorse, Suno, anything ComfyUI-driven):

**Rule**: The workflow JSON file is the single source of truth. Pipelines must LOAD the workflow file at runtime and INJECT only dynamic parameters (prompt text, seed, width/height, reference images). Never hand-translate workflow JSON into Python dict builders inside `comfyui_tools.py` or equivalent.

**Why**: When Roberto tweaks a workflow in the ComfyUI UI (changes guidance, sampler, LoRA, dimensions, adds nodes), the pipeline must pick up those changes automatically without touching code. Hand-built Python builders go stale the moment the JSON is edited and silently diverge from what's tested in the UI. Past pattern (`_qwen2512_workflow`, `_z_turbo_workflow` in `comfyui_tools.py`) is exactly what to avoid.

**How to apply**:
1. Workflow files live under `~/comfyui-workflows/<family>/<name>.json` (UI format) — Roberto edits these in ComfyUI directly.
2. UI -> API conversion is fine to do programmatically (Roberto explicitly approved). Either run conversion at runtime or save an `_api.json` next to the UI file.
3. The pipeline reads the API-format JSON, finds known nodes (CLIPTextEncode, RandomNoise, EmptyFlux2LatentImage, LoadImage, etc.) by node ID, injects runtime params, submits to `/prompt`.
4. **If a workflow needs to change**, do not edit the JSON unilaterally. Surface the proposed change to Roberto first, discuss, then apply together. Same for adding new node types, swapping checkpoints, etc.
5. Editing a UI workflow file directly IS allowed (Roberto granted permission) when there's a clear reason — but discuss first.
6. Apply the same loader pattern to ALL media pipelines, not just images. Video, audio, batch jobs — same rule.

**Concrete tool**: `~/commander/tools/comfyui_workflow.py` should host the load + inject + (optional) UI->API conversion logic, reused by every pipeline.
