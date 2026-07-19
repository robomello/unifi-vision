---
name: Headless MCP Auth for Claude Desktop (X-API-Key via mcp-remote)
description: Claude Desktop reaches mcp.synai.ai/mcp headless via X-API-Key in mcp-remote; no browser/OAuth. CF Access does not cover /mcp, so the key is the only guard.
type: project
---

**Rule:** Claude Desktop connects to the remote MCP server (https://mcp.synai.ai/mcp) fully headless — no browser login, no Google OAuth. Auth is an X-API-Key header carried by the npx mcp-remote bridge (native connectors cannot send custom headers).

**How it works:**
- Server (container `mcp-server`, source /home/mello/commander/projects/mcp-server/) accepts `X-API-Key` on /mcp. OAuth stays enabled for other clients but is unused here.
- Claude Desktop config uses `npx mcp-remote https://mcp.synai.ai/mcp --header X-API-Key:<key>` (no space after the colon — mcp-remote arg-splitting quirk). Reference config at /home/mello/_handoffs/claude_desktop_config.json; on the Mac it merges into ~/Library/Application Support/Claude/claude_desktop_config.json.
- Cloudflare Access does NOT cover /mcp — its one Access app is scoped to the literal path mcp.synai.ai/authorize only. So the API key is the SOLE guard on /mcp; there is no network-layer backstop. (Decision on 2026 setup: user chose API-key-only, declined adding a CF service-token gate.)

**How to apply:**
- The API key lives only in /home/mello/_handoffs/ files (chmod 600). Treat it as a password. If it leaks or the Mac is retired, ROTATE: new key in server env + update the Mac config.
- A static OAuth client `be8973ea3bd3ca00e474f3619c79ad83` (client_name claude-desktop-connector) was also registered in oauth.db but is dormant/unused — safe to delete if cleaning up.
- Secrets are PLAINTEXT in oauth.db client_secret column (tokens are hashed); keep that in mind for any audit.
