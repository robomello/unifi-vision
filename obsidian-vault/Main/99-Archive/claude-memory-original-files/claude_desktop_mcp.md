---
name: Claude Desktop MCP
description: Claude Desktop connects to mcp.synai.ai via mcp-remote; post-cutover runs its own OAuth 2.0 flow, no injected headers
type: reference
originSessionId: <REDACTED-UUID-4>
---
Claude Desktop is wired to the home server's MCP via `https://mcp.synai.ai/mcp` (Streamable HTTP) using the `mcp-remote` bridge (requires Node.js on Roberto's Desktop machine).

## Auth (post-OAuth cutover, 2026-04-21)
- `mcp-remote` performs its **own** OAuth 2.0 flow against the embedded AS at `mcp.synai.ai` (DCR + PKCE S256 + Google login via CF Access on `/authorize`).
- Tokens persist in `~/.mcp-auth/` on Roberto's desktop machine. First launch opens a browser once.
- No `--header` flags in the config — the Desktop config at `/home/mello/_handoffs/claude_desktop_config.json` is the canonical template and is now header-less.
- `MCP_LEGACY_AUTH=true` remains on during the cutover window so an `X-API-Key: $MCP_API_KEY` or `Authorization: Bearer $MCP_API_KEY` call still works as a break-glass.

## Desktop config locations (Roberto pastes template here)
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- Linux: (n/a; Desktop unsupported)
- Template: `/home/mello/_handoffs/claude_desktop_config.json`; previous header-full version backed up as `claude_desktop_config.<timestamp>.bak`.

## Retire sequence (after E2E test passes)
1. Flip `MCP_LEGACY_AUTH=false` in `/home/mello/docker-compose.yml`, restart `mcp-server`.
2. Revoke the CF Access service token `<REDACTED-UUID-5>` via CF API.
3. Unset `MCP_API_KEY`, `CLAUDE_DESKTOP_CF_ACCESS_CLIENT_ID`, `CLAUDE_DESKTOP_CF_ACCESS_CLIENT_SECRET`, `CLAUDE_DESKTOP_MCP_API_KEY` from `~/.env` (or leave MCP_API_KEY as a dormant break-glass; zero-op while OAuth is enforced).

## Tools exposed (unchanged)
`server_status`, `server_run_command`, `server_read_file`, `server_write_file`, `server_list_directory`, `server_docker_compose` -- source: `/home/mello/commander/projects/mcp-server/server.py`.
