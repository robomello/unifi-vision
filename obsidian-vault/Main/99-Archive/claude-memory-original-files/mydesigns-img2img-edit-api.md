---
name: MyDesigns img2img edit API
description: Wire shape + mode enum + presign-S3 upload flow for MyDesigns Dream AI image-to-image (verified GPT Image 2 working)
type: reference
---

MyDesigns Dream API supports image-to-image (edit) mode. Wired into `/home/mello/commander/tools/mydesigns_dream.py` as the `edit()` function and `--edit IMAGE` CLI flag.

**Endpoint**: POST /integrations/dreamer/dream-images (same as text-to-image; mode field switches behavior).

**Mode enum** (3 values): `TEXT_TO_IMAGE`, `IMAGE_TO_IMAGE`, `GPT_IMAGE_1_EDIT`.
- For ALL gpt-image-* engines (gpt-image-1, gpt-image-1.5, gpt-image-2, gpt-image-1-mini) use `GPT_IMAGE_1_EDIT` — the '1' in the name is legacy. Verified working with engineId=gpt-image-2.
- For non-GPT engines doing img2img use `IMAGE_TO_IMAGE`.
- IMAGE_TO_IMAGE mode requires `imageStrength` to be present and an **int 0-100** (not float — sending 0.5 fails JSON parse).

**Reference image upload** uses a different flow than the asset library:
1. POST /designs/presign-put-url?extension=.jpg → returns `{path, url, type}` (S3 presigned)
2. PUT image bytes to that S3 url with the returned content-type
3. Use the returned `path` (e.g. `design/tmp/UUID.jpeg`) in dream-images payload as `filePath` AND `filePaths[0]` (sending both is accepted; not yet verified which one MyDesigns actually reads).

**Why**: User asked for img2img with GPT Image 2. Verified end-to-end 2026-05-13 — Joel reference + sunset-beach prompt produced a clean edit in 53s, ~3 credits.

**How to apply**: Call `mydesigns_dream.edit(prompt=..., image=PATH, engine='gpt-image-2', image_strength=50, quality='medium')` or use `mydesigns_dream.py --engine gpt2 --edit PATH --strength 50 --quality medium 'prompt'`. Extra inline references (max 2) via `--reference IMG`.
