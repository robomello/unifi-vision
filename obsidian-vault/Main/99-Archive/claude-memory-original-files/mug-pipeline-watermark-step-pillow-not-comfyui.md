---
name: Mug Pipeline Watermark Step (Pillow, not ComfyUI)
description: Mug pipeline watermark step using Pillow after mockup generation, before SEO/publish. Etsy listing photos get watermarked; raw wrap designs stay clean for Printify. Config in mug_pipeline/config.py
type: project
---

# Mug Pipeline — Watermark Step

Adds branding/theft protection to Etsy listing photos in `/home/mello/commander/projects/mug_pipeline/`.

## Pillow, NOT ComfyUI

Watermark = `Image.alpha_composite()`. ComfyUI is wrong tool:

| Approach | Latency | GPU | Complexity |
|---|---|---|---|
| ComfyUI | 10s+ | yes (ties up queue) | custom workflow JSON, overkill |
| Pillow | ~5ms | no | already used by `mockup_warp.py` |

Pillow matches the existing pattern in `mockup_warp.py`.

## Pipeline Placement

```
research → generate → quality → mockup → [WATERMARK] → seo → publish
```

Mockup images are the **Etsy listing photos** — those are what need protection. **Raw wrap design stays unwatermarked** (it's uploaded to Printify for printing).

## Assets

| Asset | Path |
|---|---|
| Transparent logo PNG (RGBA) | `/data/sites/drinkwaretrove/assets/logo.png` |

Recommended ~300×300 px. Verify mode is `RGBA`:
```bash
python3 -c "from PIL import Image; img = Image.open('/data/sites/drinkwaretrove/assets/logo.png'); print(f'{img.size} mode={img.mode}')"
```

## Implementation Files

### `projects/mug_pipeline/watermark_step.py` (new, ~50 lines)

```python
def apply_watermark(mockup_path, logo_path, opacity, position) -> str:
    """Opens mockup JPEG → RGBA. Loads logo PNG (cached). Resizes logo to
    ~10% of mockup width. Applies opacity via alpha channel multiplication.
    Composites at chosen corner with padding. Saves back as JPEG (same path,
    overwrites — mockups are regenerable)."""

def run_watermark(limit, record_id) -> dict:
    """Queries NocoDB for Status=mockup_ready records.
    Parses Mockup Paths JSON list, calls apply_watermark() on each.
    Updates NocoDB with Watermarked: true.
    Returns {watermarked: N, failed: N}."""
```

CLI:
```bash
python3 -m projects.mug_pipeline watermark
python3 -m projects.mug_pipeline watermark --id 42
python3 -m projects.mug_pipeline watermark --opacity 0.25
```

### `projects/mug_pipeline/config.py` (edit, +6 lines after mockup compositing section)

```python
# -- Watermark ---------------------------------------------------------------
WATERMARK_LOGO_PATH = Path("/data/sites/drinkwaretrove/assets/logo.png")
WATERMARK_OPACITY = 0.3
WATERMARK_POSITION = "bottom-right"  # bottom-right | bottom-left | top-right | top-left
WATERMARK_PADDING_PX = 20
WATERMARK_SCALE = 0.10               # logo width = 10% of mockup width
```

## Logo Cache

Load logo once (per process) since `run_watermark` iterates many mockups. Reload only if `logo_path` mtime changes.

## Verification

- `python3 -m projects.mug_pipeline watermark --id <one record>` overwrites mockup JPEG in place
- Open the file → corner logo visible at 30% opacity, ~10% of mockup width
- NocoDB: record's `Watermarked` field flipped to `true`
- Raw wrap design (the Printify-bound file) NOT touched

## Why This Pattern Worth Saving

- Pillow >> ComfyUI for non-AI image ops (consistent rule across mug_pipeline + future projects)
- Watermark mockups, NOT raw designs — POD-printer files stay clean
- Logo path lives outside the project repo (`/data/sites/drinkwaretrove/assets/`) — usable across drinkwaretrove sub-projects
