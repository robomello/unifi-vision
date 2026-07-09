---
name: Obsidian Container
description: Obsidian at obsidian.synai.ai via Selkies streaming, CF Access Gmail-gated to robomello79
type: reference
originSessionId: <REDACTED-UUID-27>
---
## Obsidian -- Deployed (2026-04-16)

- **Container**: `obsidian` (image `lscr.io/linuxserver/obsidian:latest`, 3.68GB)
- **Local bind**: `127.0.0.1:8099 -> 3000/tcp`
- **Network**: `n8n-net` (required for CF Tunnel reach)
- **Public URL**: `https://obsidian.synai.ai` (CF Tunnel route)
- **Access**: Gmail-gated to `robomello79@gmail.com` only (CF Access app `<REDACTED-UUID-28>`, policy `<REDACTED-UUID-29>`)
- **Streaming**: Selkies (WebSocket/WebRTC), not KasmVNC anymore -- linuxserver migrated
- **Encoder**: x264enc CPU, display starts at 1024x768 (CUSTOM_RES_W/H env ignored by new Selkies backend; resize from client-side UI)
- **Vault**: `/home/mello/obsidian-vault` (host) -> `/vaults` (container)
- **Config**: `/home/mello/.config/obsidian-container` (host) -> `/config` (container)

## Plugins
- **objects** v1.0.18 (Finn-Kraemer/obsidian-objects) -- installed to `.obsidian/plugins/objects/`, enabled in `community-plugins.json`. Built from source (npm run build -> release/main.js).

## Previous black-screen issue (2026-04-07)
Was on older KasmVNC backend. New Selkies backend (2026-04-16) uses x264enc + WebSocket. Resolution starts at 1024x768 -- adjust from client sidebar, not CUSTOM_RES_W env.

**How to apply:** When Roberto mentions Obsidian, point to https://obsidian.synai.ai. To install more plugins: clone repo, `npm install && npm run build`, copy `release/main.js` + `manifest.json` to `/home/mello/obsidian-vault/.obsidian/plugins/<id>/`, add `<id>` to `community-plugins.json`, restart vault.
