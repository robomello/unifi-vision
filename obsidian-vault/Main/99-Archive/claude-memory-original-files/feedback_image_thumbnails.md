---
name: Image thumbnails
description: Display large generated images via downscaled thumbnails (Pillow → JPEG ≤360px), full-size only on click. Don't CSS-scale 2 MB PNGs.
type: feedback
originSessionId: <REDACTED-UUID-16>
---
When showing user-generated images on a web UI page (job detail, gallery, dashboard), don't display the raw output as the inline element. Generate a smaller variant (Pillow → 360px wide JPEG, ~50-70 KB) at write time and serve via a `?thumb=true` query param on the same media endpoint. Use the full-size only when the user clicks/zooms.

**Why:** Roberto called this out as a "basic thing" I should have caught. Loading a 2 MB PNG just to render at 160px in the dashboard wastes bandwidth, makes the page feel disproportional (huge images dominating tiny descriptions), and slows polling pages where the image refreshes frequently.

**How to apply:** For any pipeline that renders images for later UI display:
1. After image render completes, also write `image_thumb.jpg` (Pillow LANCZOS, quality 82, ~360px wide).
2. Media-serving endpoint accepts `?thumb=true` (or similar) and serves the JPEG with `image/jpeg` MIME.
3. Lazy-build the thumb on first request if missing (covers pre-existing images without re-running the pipeline).
4. Backfill existing files with a one-shot Pillow loop when adding the feature.
5. CSS: fixed display width (e.g., 160px) on the `<img>`, `cursor: zoom-in`, wrapped in `<a target="_blank" href={full_url}>`.
