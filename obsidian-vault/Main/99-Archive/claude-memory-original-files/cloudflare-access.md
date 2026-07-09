---
name: cloudflare-access
description: Cloudflare API access pattern -- tokens, account ID, tunnel ID, and how to manage tunnel routes
type: reference
---

Cloudflare API is accessible via env vars in `/home/mello/.env`:

- `CLOUDFLARE_API_TOKEN` -- works for tunnel config management (verified 2026-03-21)
- `CLOUDFLARE_ACCOUNT_ID` = `<REDACTED-HEX32-2>`
- `CLOUDFLARE_ZONE_ID` -- for DNS operations
- `CF_API_KEY` -- Global API Key (not working, email pairing attempted, auth fails)

**IMPORTANT:** The `cfut_` prefixed token is a Cloudflare Tunnel User Token. It CANNOT be edited to add DNS/Workers permissions. For DNS:Write or Workers:Write, create a SEPARATE API token via CF dashboard.
- Tunnel ID: `<REDACTED-UUID-2>`

**Auth pattern:** `Authorization: Bearer $CLOUDFLARE_API_TOKEN`

**Tunnel config API:**
- GET: `https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/cfd_tunnel/$TUNNEL_ID/configurations`
- PUT: same URL with `{config: {ingress: [...]}}` body

**Identity Providers (as of 2026-04-03):**
- One-Time PIN (email OTP) -- ID: `<REDACTED-UUID-8>`
- Google OAuth -- ID: `<REDACTED-UUID-9>`, Client ID: `<REDACTED-OAUTH_CLIENT-1>`

Roberto prefers Google OAuth (one-click) over email OTP (annoying). Both are active.

**How to apply:** When any task involves Cloudflare (tunnel routes, DNS, etc.), use the `cloudflare-agent`. Don't ask the user if you have access -- you do.
