---
name: FB Monitor
description: Facebook image monitor Telegram bot -- gallery-dl auto-downloads, @fb_extract_bot, NocoDB tracking, 10-min scheduler
type: project
---

## Facebook Image Monitor

Telegram bot that monitors Facebook profiles for new images and auto-downloads them via gallery-dl.

- **Location**: `/home/mello/commander/projects/fb-monitor/`
- **Container**: `fb-monitor` (Python 3.11-slim, no GPU)
- **Telegram bot**: `@fb_extract_bot` (token: `TELEGRAM_FB_EXTRACTOR_TOKEN`)
- **Data**: `/data/fb-monitor/images/facebook/{username}/`
- **NocoDB table**: `fb_profiles` (ID: `mxtecr2rj34i56t`, Commander base)
- **Deployed**: 2026-03-29

## Architecture

6 Python files: config.py, profiles.py, downloader.py, scheduler.py, bot.py
- gallery-dl with `--destination` and `--download-archive` for dedup
- NocoDB for profile state (not local JSON)
- 10-minute check interval, sequential profile downloads
- Cookies: mounted read-only from `~/facebook_cookies.txt`

## Commands

`/add <url>`, `/remove <username>`, `/list`, `/check [username]`, `/status`
Also accepts bare Facebook URLs (auto-triggers /add).

## Key env vars in .env

- `NOCODB_FB_PROFILES_TABLE_ID=mxtecr2rj34i56t`
- `TELEGRAM_FB_EXTRACTOR_TOKEN` (already existed)

## Seeded data

Rizan Dadoush: 389 images migrated from ~/Downloads/rizan_dadoush/, NocoDB row active.
