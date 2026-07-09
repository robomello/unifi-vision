---
name: Joel canonical anchor locked = Qwen Image 2512
description: Joel hero ref locked to joel_qwen2512.png. Training-set + LoRA bootstrap planned next.
type: project
---

**Locked 2026-05-11.** Joel's canonical look is `joel_qwen2512.png` — generated with Qwen Image 2512. Recorded in `bible/vloggers.json` under Joel's entry:
```json
"canonical_hero_ref": ".state/hero_refs/joel/joel_qwen2512.png",
"canonical_model": "qwen_image_2512"
```
Bible manifest re-locked at 2026-05-11T20:50 UTC.

**Why:** Roberto picked Qwen 2512 over Flux 2 Dev, ChatGPT, and Z-Image Turbo (4 variants were rendered for comparison; see `/hero_refs/joel/` on the public viewer). The Qwen 2512 result best matched the desired vlogger look — warm documentary cinematography, mid-30s American man with disheveled brown hair, hazel eyes, period-adjacent outfit base.

**Next: train a LoRA on Joel.** Standard franchise scale will need ~3780 scene plates (42 scenes × 30 episodes × 3 channels). Per-scene face-consistency requires a per-vlogger LoRA. Bootstrap plan:
1. Generate a diverse training set of Joel (60-80 images) with Qwen 2512 + Lightning LoRA for speed
2. Optional pass: face-swap-enforce the anchor identity via existing `Face Swap PixelSmile Workflow.json` + `joel_qwen2512.png`
3. Cull keepers
4. Train LoRA via local `ai-toolkit` (RTX PRO 6000 96GB has headroom)
5. Repeat for Cintia and Claudio once their anchors are picked

**How to apply:** Until the Joel LoRA exists, any prompt that needs to depict Joel must reference `visual_reference_prompt` from `bible/vloggers.json` verbatim. After LoRA exists, prompts can shrink to e.g. `joel_marlowe, [scene]` with `<lora:joel_v1:0.85>`.
