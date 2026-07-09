---
name: Street-camera tuning correction: 0.40 + box-area + delivery-truck-only (supersedes 0.25)
description: CORRECTION: street-camera MIN_CONFIDENCE=0.40 (not 0.25), MIN_BOX_AREA_FRAC=0.0015, delivery alerts require truck-type; verify accuracy by VIEWING snapshots
type: project
---

Correction to the earlier street-camera fix note. MIN_CONFIDENCE=0.25 was TOO LOW: once frames flowed it produced false positives (GDINO boxes on brick/foliage and tiny distant blobs) and gemma3:4b stamped "UPS" on ordinary cars, spamming Telegram alerts ("none of the images sent were accurate").

Final tuned values, verified by VIEWING live snapshots in /data/street-camera/images on 2026-06-21:
- MIN_CONFIDENCE=0.40 (was 0.25); GDINO_BOX_THRESHOLD=0.25
- MIN_BOX_AREA_FRAC=0.0015 — reject any detection whose box is < 0.15% of frame AREA. Area-based (not per-dimension) so a narrow distant person is kept while tiny blobs are dropped.
- Delivery-brand alerts now require object_type in DELIVERY_VEHICLE_TYPES={"truck"} (vans map to truck). A "car" tagged with a delivery brand is a gemma3:4b mis-read and must NOT alert.
- VLM prompt hardened: report a delivery brand ONLY if the logo/livery is clearly visible; never guess from color.

KEY LESSON: verify detection ACCURACY by opening the annotated snapshots (the Read tool renders images), not just by counting detections or watching "Saved:" logs. Counts looked fine at 0.25 while every alert image was junk. All knobs are env-tunable in docker-compose.yml (no rebuild).
