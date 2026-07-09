---
name: Joel LoRA v3 - synthetic subject photoreal recipe
description: Research-backed pipeline for training character LoRAs from AI-generated subjects without the v2 plastic-skin failure mode
type: project
---

# Joel LoRA v3 — synthetic subject photoreal recipe

Recipe distilled from deep research (Apatero, civitai, AI-toolkit community) for training a character LoRA from an AI-generated person (Joel via ChatGPT image gen). Solves the v2 failure mode where output looked like glossy AI portraits instead of camera photos.

**Why this matters:** Real-subject LoRAs can use real camera photos as dataset, so realism comes for free. Synthetic subjects have no real photos — every pixel in the dataset is AI-painted. Without intervention the LoRA learns "AI-painted Joel" and reproduces that look at inference.

## Pipeline (synthetic-subject playbook)

1. **Single master image** → upscale with face-specialist (4xFFHQDAT) → square 1024×1024 crop
2. **Variant generation** via Qwen Image Edit 2511 + multiple-angles LoRA — 25-30 angle/light/wardrobe variants from one master
3. **De-AI pre-pass** — img2img at denoise 0.20-0.30 using Qwen Image 2512 (NOT edit) with realism LoRAs to inject camera-physics signals (pores, grain, lens feel)
4. **Identity-isolated captions** via JoyCaption — short (30-50 words), describe scene/clothing/light but NEVER face/eyes/skin/hair. Trigger nonsense token (`ohwx_joel` not `joelmarlowe`).
5. **Training** in ai-toolkit with research-backed config below
6. **Inference** with character LoRA stacked with realism LoRAs

## Anti-AI sampling (CRITICAL)
- Sampler: `deis` + scheduler `beta` — community-validated anti-waxy combo for Qwen/Flux
- Alt: `res_2` + `bong_tangent` (Qwen plastic-skin fix per ApateroRealism research)
- AVOID: `euler` + `simple` at CFG 4 → produces glossy rendered output
- CFG: **2.5-3.0** (distilled-guidance sweet spot). Higher = more directed = more rendered.
- Negative prompt: explicit anti-AI list (plastic skin, smooth AI skin, beauty filter, airbrushed, doll-like, rendered, CGI, glossy, oversaturated, studio portrait lighting). NOT ConditioningZeroOut.

## Realism LoRA stack (REQUIRED — not optional)
- SamsungCam UltraReal — civitai 1551668, Qwen Image variant — @ 0.6-0.7 for de-AI, @ 0.60 for inference
- GrainScape UltraReal — civitai 1332651, Qwen Image variant — @ 0.30 throughout
- Without these LoRAs, the de-AI pass has only sampler+prompt to work with, which is insufficient.

## Training config deltas (v2 → v3)
| Setting | v2 (bad) | v3 (good) | Why |
|---|---|---|---|
| rank / alpha | 64 / 64 | 32 / 16 (2:1) | Apatero photoreal recipe; high rank overfits AI tells |
| batch size | 4 | 1 | Per-sample gradient quality |
| resolution | [768, 1024] | [1024] strict | One bucket prevents face-pixel inconsistency |
| timestep weight | default | sigmoid | Better for character identity preservation |
| LR schedule | constant | cosine + 250 warmup | Smooth convergence |
| transformer quant | qfloat8 | unquantized | qfloat8 was the v2 plastic-skin culprit |
| EMA | off | on, decay 0.99 | Stable inference checkpoint |
| steps | 2000 | 2500 | Headroom for the smaller rank |
| trigger | semantic name | nonsense (`ohwx_joel`) | Avoid base-model priors |

## Inference stack
- Character LoRA @ 0.80
- SamsungCam UltraReal @ 0.60
- GrainScape UltraReal @ 0.30
- deis/beta + CFG 3.0 + same anti-AI negative

## Caption strategy
- DO NOT describe face/eyes/nose/skin/hair/age/ethnicity — LoRA learns those
- DO describe: scene, clothing, lighting, pose, mood, framing
- Length: 30-50 words
- Format: `<trigger>, <scene description>`
- max_new_tokens=110 in JoyCaption (was 400 in v2, produced over-detailed captions)

## Honest ceiling
- Real-photo subjects: can fool casual viewers and most automated detectors
- Synthetic-subject ceiling: "convincing candid AI photo that doesn't read as AI at a glance" — NOT forensic-grade. Model collapse research says >2% AI-on-AI training degrades; we mitigate by de-AI'ing the dataset before training, never eliminate.

## File anchors
- Plan: `/home/mello/.claude/plans/joel-lora-v3-realism-upgrade.md`
- Pipeline: `/home/mello/commander/projects/joel_lora_v3/`
- Training config: `/home/mello/ai-toolkit/config/joel_lora_qwen_2512_v3.yaml`
