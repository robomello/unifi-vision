---
name: ComfyUI V3 DynamicCombo API serialization (dot-prefixed sub-inputs)
description: API-format prompts: dynamic combo = plain string + style.subkey dot-prefixed inputs, not a dict
type: reference
---

When queueing ComfyUI API-format prompts that use V3 DynamicCombo inputs (COMFY_DYNAMICCOMBO_V3, e.g. the style input on Ideogram4PromptBuilderKJ from comfyui-kjnodes), do NOT pass a dict. Pass the selected option key as a plain string plus each sub-input as a separate dot-prefixed input key. Example: "style": "photo" and "style.photo": "candid smartphone photo.". Passing {"style": {...}} validates but fails at execute() with 'missing 1 required positional argument'. Parsing logic: /app/comfy_api/latest/_io.py (finalize_prefix joins with dots). Verified on ComfyUI 0.24.1, 2026-06-10, first successful Ideogram 4 run (dual-model fp8, 23s on the Blackwell).
