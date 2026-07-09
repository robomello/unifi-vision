---
name: Conectitude Pipeline
description: Gisele's Portuguese parenting YouTube channel video pipeline -- takes Parentitude URLs, creates original PT-BR videos
type: project
---

Conectitude is Gisele's Portuguese parenting YouTube channel. Pipeline takes a Parentitude (English) video URL, extracts the TOPIC (not script), writes original PT-BR content, and produces a full video.

**Why:** Gisele wants to create high-quality parenting content in Brazilian Portuguese, inspired by (but not translated from) English parenting channels.

**How to apply:** When Roberto mentions Conectitude, Gisele's channel, or Portuguese parenting videos, this pipeline is the tool.

## Key Locations
- Code: `/home/mello/commander/projects/conectitude/` (13 Python modules)
- Data: `/data/sites/conectitude/` (voices, music, fonts, jobs)
- Font: Nunito variable font at `/data/sites/conectitude/fonts/Nunito-Regular.ttf`

## NocoDB Tables
- ConectitudeJobs: `mz5nnrl9w05gghv`
- ConectitudeScenes: `m8hdqvvagh6bue9`

## Pipeline Phases
1. Topic extraction (yt_extract.py + Claude opus)
2. Visuals (ComfyUI Qwen2512 GPU 1) + Audio (F5-TTS GPU 0) in parallel
3. Video clips (Ken Burns + Kling 2.1 Pro for heroes)
4. Assembly (FFmpeg concat + subtitles)
5. Upload (YouTube unlisted + SEO)

## Blocking (as of 2026-03-26)
- Gisele's 30s voice sample needed for F5-TTS cloning (using Kokoro fallback until then)
- All 3 fallback music tracks generated: gentle, upbeat, emotional

## CLI
```bash
cd /home/mello/commander/projects
python -m conectitude "https://youtube.com/watch?v=..." --skip-upload -v
```
