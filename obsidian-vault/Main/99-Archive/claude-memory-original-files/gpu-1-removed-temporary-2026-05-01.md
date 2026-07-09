---
name: GPU 1 removed (temporary, 2026-05-01)
description: Single-GPU server as of 2026-05-01; GPU 1 references in context.md are stale
type: project
---

GPU 1 (secondary RTX PRO 6000 Blackwell 96GB, 300W) was removed on 2026-05-01. Marked as temporary ("for now") by Roberto.

**Why:** Hardware change. No reason given.

**How to apply:**
- Treat the home server as a single-GPU box (GPU 0 only) until Roberto confirms otherwise.
- Do NOT use `device_ids: ['1']` in any new docker-compose service.
- The rules file `~/.claude/rules/context.md` still lists GPU 1 and assigns these services to it: n8n, ollama, factory-agent, commander, street-camera, casa-api. That section is now stale.
- Before scheduling parallel ComfyUI / heavy inference, assume only GPU 0 is available.
- If a task requires GPU 1, surface it to Roberto rather than silently failing or routing to GPU 0 (could OOM the primary).
