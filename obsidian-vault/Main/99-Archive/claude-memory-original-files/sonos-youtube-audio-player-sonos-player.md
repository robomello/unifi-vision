---
name: Sonos YouTube Audio Player (sonos-player)
description: Home-built tool to extract YouTube audio via yt-dlp and play it on Sonos speakers; known gotchas and HA integration idea
type: reference
---

**sonos-player** — home-built FastAPI service that extracts YouTube audio and streams it to Sonos speakers.

- **Location**: `/home/mello/commander/projects/sonos-player` (app.py + static/index.html web UI)
- **Runs as**: Docker container `sonos-player`, `network_mode: host`, port 8767, host IP `192.168.3.60`. LAN/server-only — no Cloudflare route.
- **How it works**: pick a Sonos speaker + paste a YouTube URL in the web UI -> backend runs `yt-dlp -x --audio-format mp3` -> caches the MP3 in `data/audio/` (bind-mounted, persists across container restarts) named by MD5 hash of the source URL -> uses the `soco` library's `play_uri()` to stream it to the chosen Sonos zone from the local `/media/{filename}` endpoint.
- **Known Sonos zones**: Gym, Kitchen, Living Room, Master Bedroom, Patio, Shop.
- **Gotcha — speaker drops off the dropdown**: `discover_sonos()` only does 3s of UPnP multicast discovery before falling back to a hardcoded IP list, and the in-memory `_zones` cache doesn't auto-refresh on a failed discovery. A speaker can silently vanish from `/api/speakers`. Fix: `POST /api/refresh` (or reload the web UI) — no container restart needed.
- **Gotcha — can't identify cached tracks later**: downloaded files are named only by MD5 hash of the URL, no title or ID3 metadata is embedded. As of 2026-07-02 only one track has ever been cached (`a549c45b5d55.mp3`, also saved with a friendly copy `Master-Bedroom-track-2026-04-18.mp3` in the same folder for reference).
- **Home Assistant**: real HA instance lives at `http://192.168.2.120:8123` (token already used by `garden-telegram`). Not yet integrated with sonos-player. Considered approach: HA `rest_command:` hitting sonos-player's `/api/play` directly (Sonos logic already lives server-side), rather than building a full custom HA media_player integration.
