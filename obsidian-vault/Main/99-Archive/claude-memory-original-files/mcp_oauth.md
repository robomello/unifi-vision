---
name: MCP OAuth 2.0
description: Roberto's MCP server (mcp.synai.ai) runs an embedded OAuth 2.0 AS+RS per MCP spec 2025-06-18. Tokens in sqlite. CF Access gates only /authorize via Google OAuth.
type: reference
originSessionId: <REDACTED-UUID-25>
---
# MCP OAuth 2.0

`mcp.synai.ai` speaks OAuth 2.0 per MCP spec 2025-06-18 (RFC 7591 DCR, RFC 7636 PKCE S256, RFC 9068 + 9728). Same process is AS + RS.

## URLs
- Issuer: `https://mcp.synai.ai`
- Resource: `https://mcp.synai.ai/mcp`
- Metadata: `/.well-known/oauth-authorization-server`, `/.well-known/oauth-protected-resource/mcp`
- Endpoints: `/register` (DCR), `/authorize`, `/token`, `/revoke`, `/mcp` (bearer-gated)

## Scope
Single scope `mcp:full`. PKCE S256 required. Opaque tokens, sha256-hashed at rest. Access TTL 1h, refresh TTL 30d, code TTL 10m. Refresh rotation on every use. Audience = `https://mcp.synai.ai/mcp`.

## Identity
Login delegated to CF Access on `/authorize` path **only** (App id `<REDACTED-UUID-26>`, aud `b533f207cf36473f88c9e790e9e61c5c56246cbb49b01ed4c671b42be7f63968`, Google IdP `<REDACTED-UUID-9>`). Allowed emails hard-coded: `mello_roberto@hotmail.com`, `robomello79@gmail.com`. `CfAccessIdentityMiddleware` in `server.py` verifies the JWT via team JWKS and sets a ContextVar read by `provider.authorize()`.

## Files
- `/home/mello/commander/projects/mcp-server/server.py` — FastMCP wiring + middleware stack (HostFix → LegacyAuthShim → CfAccessIdentity → mcp.streamable_http_app()).
- `/home/mello/commander/projects/mcp-server/oauth_provider.py` — `HomeServerOAuthProvider`, `SqliteStore`, `CfAccessVerifier`, `init_db`.
- sqlite at host `/home/mello/commander/projects/mcp-server/data/oauth.db` (mounted at `/app/data/oauth.db`).
- docker-compose service `mcp-server` has env `MCP_OAUTH_ENABLED`, `MCP_LEGACY_AUTH`, `MCP_ISSUER_URL`, `MCP_RESOURCE_URL`, `MCP_DB_PATH`, `MCP_CF_TEAM_DOMAIN`, `MCP_CF_ACCESS_AUD`.

## Legacy auth (MCP_LEGACY_AUTH=true)
`load_access_token` accepts `MCP_API_KEY` as a synthetic AccessToken. `X-API-Key` header is rewritten to `Authorization: Bearer` by `LegacyAuthShim`. Used for transition — flip `MCP_LEGACY_AUTH=false` and revoke the CF Access service token `<REDACTED-UUID-5>` once Desktop + Claude.ai are confirmed working.

## Key rotation
Opaque tokens regenerate on every refresh. To rotate `MCP_API_KEY`: generate 48 random bytes → update `/home/mello/.env` → `docker compose up -d mcp-server`. After cutover, preferred path is to unset `MCP_API_KEY` and set `MCP_LEGACY_AUTH=false`.

## Rollback
Set `MCP_OAUTH_ENABLED=false` and `MCP_LEGACY_AUTH=true` in compose → restart. CF snapshot for old app at `/home/mello/.claude/plans/artifacts/mcp-access-*.before.json`.
