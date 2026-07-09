---
name: Street-camera FINAL: MIN_CONFIDENCE=0.45 (81% measured) + qwen2.5vl VLM + eval_precision.py
description: Measured solution: MIN_CONFIDENCE=0.45 gives 81% detection precision; VLM=qwen2.5vl:7b (gemma3:4b hallucinated brands); re-run eval_precision.py to measure
type: project
---

Final tuned street-camera detection, set from a MEASURED precision sweep (not eyeballing) on 2026-06-21.

TOOL: commander/projects/street-camera/eval_precision.py — judges every saved detection by cropping to its DB bbox (+context, top kept at box edge to exclude the drawn label) and asking a LOCAL VLM (qwen2.5vl:7b via ollama 127.0.0.1:11434, FREE) what the crop really is, then sweeps confidence thresholds. Calibrated 6/6 on known cases. Re-run it any time to re-measure precision (no cloud cost).

MEASURED precision curve over 132 real detections: conf>=0.40 -> 70%, 0.45 -> 81%, 0.50 -> 83%, 0.60 -> 92%, 0.70 -> 100%. Chose MIN_CONFIDENCE=0.45 (lowest threshold clearing the 75% target, max coverage). Supersedes the earlier 0.40 value.

VLM: switched OLLAMA_VLM_MODEL gemma3:4b -> qwen2.5vl:7b. gemma3:4b hallucinated delivery brands (eval: 23 brand flags, 1 real = 4%). qwen2.5vl:7b correctly abstains (it is also the eval judge). Verified live: new detections brand=none, 0 VLM errors, qwen2.5vl loaded 100% GPU.

LESSON: build a measured eval with a local VLM judge before tuning thresholds; counts/logs alone hid that every brand was wrong. All knobs env-tunable (MIN_CONFIDENCE, MIN_BOX_AREA_FRAC, OLLAMA_VLM_MODEL) — no rebuild.
