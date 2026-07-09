---
name: DreamVault Image Generator Bot
description: Telegram image gen bot at /home/mello/commander/projects/dreamvault-gen/. 10 models (5 local ComfyUI + 5 cloud MyDesigns/Grok/Fal.ai). Container: dreamvault-gen on n8n-net.
type: project
---

## DreamVault Image Generator Telegram Bot

**Path:** /home/mello/commander/projects/dreamvault-gen/
**Container:** dreamvault-gen (running, up 45+ hours)
**Port:** None exposed (Telegram polling bot, no HTTP server)
**Network:** n8n-net
**Status:** Active

### What It Does
Telegram bot for AI image generation. Users send text prompts and select from 10 models:
- **Local (ComfyUI on RTX PRO 6000):** Qwen 2512, Flux 2 Dev, Flux 2 Klein, Z-Image, Ideogram 4
- **Cloud (MyDesigns/Grok/Fal.ai):** Nano Banana Pro 2, GPT Image 2, Grok Imagine Pro, Flux 2 Edit

### Features
- Inline keyboard UI for model/ratio/style selection
- Image-to-image with reference photos
- Claude-powered prompt editing (claude --print --model sonnet inside container)
- Spicy/Explicit style modifiers
- Auto-unloads VRAM after each generation via ComfyUI /free endpoint

### Key Files
- bot.py — Main Telegram bot (712 lines), python-telegram-bot framework
- imagegen.py — Generation backend (393 lines), unified async interface for local + cloud
- mydesigns_client.py — Pure HTTP MyDesigns client (280 lines), Ory Kratos two-step login
- config.py — Config from env vars
- Dockerfile — Python 3.11-slim

### Env Vars
DREAMVAULT_GEN_TOKEN, MYDESIGNS_EMAIL, MYDESIGNS_PASSWORD, KIE_API_KEY (Grok), FAL_KEY, COMFYUI_API_URL=http://comfyui:8188, PROMPT_EDIT_MODEL=sonnet

### Gotchas
- Allowed user: Telegram user ID 1359185565 only
- Ideogram 4 local has baked-in safety filter (returns gray card for NSFW prompts)
- Mounts: /home/mello/commander/tools (ro), ComfyUI input/output, ~/.claude dir (rw)

Why: dreamvault was a MISSING SOURCE in consolidated memory. This is the primary image generation Telegram bot.

How to apply: When asked to generate images via Telegram or when Roberto mentions DreamVault, this is the bot. Container is dreamvault-gen on n8n-net.
