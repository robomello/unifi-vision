---
name: MyDesigns Dream AI Integration
description: MyDesigns.io client at /home/mello/commander/tools/mydesigns_dream.py. 25+ engines, Ory Kratos auth, GPT Image 2 edit gotchas. Agent: mydesigns-agent (Haiku).
type: reference
---

## MyDesigns Dream AI Integration

**Type:** CLI tool + Claude Code agent (NOT a service/container)
**Status:** Active (core infrastructure for all image generation)

### Paths
- Agent: /home/mello/.claude/agents/mydesigns-agent.md
- Primary tool: /home/mello/commander/tools/mydesigns_dream.py (853 lines)
- Auth module: /home/mello/commander/tools/mydesigns_auth.py (391 lines)
- DreamVault client: /home/mello/commander/projects/dreamvault-gen/mydesigns_client.py (280 lines)

### What It Does
Client library and agent for MyDesigns.io Dream AI image generation API. Supports 25+ engines:
- Flux 2 (Max, Dev, Klein), Nano Banana (Pro, Pro 2), GPT Image 1/2
- Ideogram (3, 4), IMAGEN, Seedream, DALL-E 3, Recraft

Features: batch generation from prompt files, image-to-image editing (GPT Image 2 only), asset upload, credit management.

### Authentication
Ory Kratos two-step login at accounts.mydesigns.io (email first, then password). Pure HTTP, no Playwright needed. Auto session refresh.
- Credentials from ~/.env: MYDESIGNS_EMAIL and MYDESIGNS_PASSWORD
- Cookies stored at /tmp/mydesigns-cookies.json (ephemeral)
- Session cookie: ory_session_upbeatkepler067srv1d1e

### Key Gotchas
- GPT Image 2 edit mode: ONLY gpt-image-2 engine allowed (Roberto directive 2026-05-13)
- Edit upload uses presigned S3 PUT (/designs/presign-put-url), NOT /designs/upload-temp-file
- Wire shape for edit: mode='GPT_IMAGE_1_EDIT' (legacy enum name), engineId='gpt-image-2'
- GPT Image 2 ratios: ONLY 2:3, 1:1, 3:2 (9:16 causes HTTP 500)
- Sequential generation only — no parallel
- Default output dir: /mnt/synology/ComfyUI/MyDesigns
- Agent model: Haiku (cheap, fast)

Why: mydesigns was a MISSING SOURCE in consolidated memory. This is the core image generation client used by DreamVault and agents.

How to apply: When generating images via MyDesigns or when the mydesigns-agent is invoked, use mydesigns_dream.py. Auth is automatic via Ory Kratos.
