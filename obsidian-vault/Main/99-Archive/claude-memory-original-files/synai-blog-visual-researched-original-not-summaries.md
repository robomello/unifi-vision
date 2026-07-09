---
name: SynAI blog: visual, researched, original (not summaries)
description: Roberto wants synai.ai posts rich/visual/primary-sourced, not derivative text summaries; build with node 22
type: feedback
---

Roberto called the first two synai.ai blog posts "lame" (welcome.md + a book-report summary of an Anthropic post). For the blog he wants: original takes tied to his actual stack, deep primary-source research with citations (verify every stat, never repeat a video/secondary number as fact), and rich visuals (hero + inline concept images via local ComfyUI + hand-built theme-matched SVG diagrams + data tables). Theme is GitHub-dark (#0d1117 bg, #79c0ff/#1f6feb accent, #e6edf3 text); SVGs must be valid XML (escape & as &amp;).

**Why:** he found derivative, text-only posts weak and explicitly asked for more detail, research, and images.

**How to apply:** writing for synai.ai = lead with his analysis, verify claims against the actual papers (spin up a research subagent), and make it visually dense.

Project facts: posts live in commander/projects/synai-blog (Astro, content collection src/content/blog/*.md). heroImage frontmatter is a relative path to src/assets/blog/. Inline raster images go in src/assets/blog/ (../../assets/...); SVG diagrams go in public/blog/ referenced as /blog/x.svg. Build needs node >=22.12 — host node is 20, use nvm: PATH=/home/mello/.nvm/versions/node/v22.22.1/bin. `npm run build` -> dist/, served read-only by the synai-blog nginx container at synai.ai (apex tunnel, host port 8068). No container restart needed after rebuild. ComfyUI for these images: reach it at comfyui:8188 from inside the network, download results via /view (the COMFYUI_OUTPUT_DIR disk-path return is unreliable cross-container).
