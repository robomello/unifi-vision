---
name: Time-Travel Franchise: viewer + bot wired 2026-05-11
description: franchise.synai.ai public viewer + @Commander_Mello_bot repurposed as franchise Claude Code terminal.
type: project
---

**Wired 2026-05-11.** Three new pieces stand up the Time-Travel Vlogger Franchise for daily ops:

**Public viewer** — `https://franchise.synai.ai`
- nginx:1.27-alpine static server in `franchise-viewer` container (docker-compose service), on `n8n-net`
- Read-only mounts of `bible/`, `.state/stories/`, `.state/hero_refs/`, `.state/runs/`
- Config: `/home/mello/commander/projects/franchise-viewer/nginx.conf`
- Tunnel ID `<REDACTED-UUID-2>` (production CF tunnel under Robomello79@gmail.com's Account, same one running n8n/nocodb/etc.); franchise.synai.ai DNS record id `<REDACTED-HEX32-3>`
- Use case: send a public URL to a collaborator to view a generated `merged.json` or vlogger anchor refs

**@Commander_Mello_bot** — repurposed from general image-gen to franchise-only Claude Code terminal
- Container `image-telegram` (service name kept for env-var continuity with `TELEGRAM_IMAGE_TOKEN`)
- Working dir locked to `/home/mello/commander/projects/time-travel-franchise/`
- Old image-gen `bot.py` backed up to `bot.py.bak-imagebot`
- New `bot.py` exposes `/channels /status /smoke /run /story /viewer /stop /new /model /end /sessions`; plain text routes to `claude --print` in franchise cwd; shortcuts `! > ? @` preserved from claude-telegram style
- No more "Which model? Z-Image Turbo / Flux 2 Dev" prompt on plain text — image-gen pipeline entirely stripped

**Why:** Roberto asked for public visibility for franchise content and a bot dedicated to running Claude Code against the 3 channels. Wanted `image-telegram`'s auto image-prompt behavior killed.

**How to apply:**
- For viewer changes: edit `nginx.conf`, restart `franchise-viewer` container (compose changes need `stop && rm && up -d`)
- For bot changes: edit `image-telegram/bot.py`, then `docker compose build image-telegram && docker stop image-telegram && docker rm image-telegram && docker compose up -d image-telegram`
- Adding more public paths to viewer: extend the `location /<x>/` block in nginx.conf and add a bind-mount in docker-compose
- If you ever rotate `TELEGRAM_IMAGE_TOKEN`: same env var still drives this bot, just update `.env` and restart
