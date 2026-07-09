---
name: synai.ai blog: Obsidian publish pipeline
description: Obsidian->Astro pipeline live: author in Main/60-Blog, ./publish.sh syncs+builds; manifest-owned, idempotent
type: project
---

Obsidian->Astro publishing pipeline is BUILT and verified (2026-06-10), replacing the previous 'pipeline TODO' gap.

- Author notes in ~/obsidian-vault/Main/60-Blog/ (template: _TEMPLATE.md; images in _attachments/).
- Frontmatter: title/description/date required; publish: true gates; optional slug/cover/updated/tags; draft: true blocks.
- Publish: cd /home/mello/commander/projects/synai-blog && ./publish.sh (or npm run publish). Flags: --dry-run, --sync-only.
- Pipeline (pipeline/sync.py + transform.py, stdlib+PyYAML): maps date->pubDate, updated->updatedDate, cover->heroImage; rewrites [[wikilinks]] to /blog/<slug>/ (unresolved -> plain text); copies ![[image]] embeds to src/assets/blog/<slug>/; strips |size hints.
- Manifest-owned (pipeline/.manifest.json): never touches hand-authored posts; slug collision with one is a hard error. Idempotent re-runs; unpublish removes post+assets and publish.sh verifies 404.
- nginx serves bind-mounted dist/, so npm run build IS the deploy. 42 pytest tests, 97% coverage (pipeline/tests).
- Lifecycle proven live: publish -> 200 with image, edit -> in-place update, unpublish -> 404; 4 pre-existing posts unaffected.
