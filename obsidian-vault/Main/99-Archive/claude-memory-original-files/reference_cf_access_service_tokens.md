---
name: CF Access Service Token Policy Structure
description: Service-token policies on CF Access apps must use decision "non_identity" — "allow" silently redirects to IdP login
type: reference
originSessionId: <REDACTED-UUID-32>
---
# CF Access Service Token Policies

For server-to-server auth (e.g. Otto → home server APIs via `*.synai.ai`), Access policies must be configured specifically for service tokens.

## The gotcha
A policy with `decision: "allow"` + `include: [{"service_token": {...}}]` looks correct but returns `auth_status: NONE` and 302-redirects to the IdP login — even though the JWT shows `service_token_status: true`.

CF Access only evaluates service tokens when the policy's `decision` is `"non_identity"`. The `"allow"` decision requires an identity (user session).

## Correct policy payload
```json
{
  "name": "Otto service token",
  "decision": "non_identity",
  "include": [
    {"service_token": {"token_id": "<service_token_UUID_not_client_id>"}}
  ]
}
```

`token_id` must be the service token's `id` field (UUID), not its `client_id`.

## How to apply
When creating CF Access protection for any server-side caller, set `decision: "non_identity"`. Only use `"allow"` when the requester is a human going through Google OAuth/OTP.

Verified working for `llm.synai.ai` (Ollama) on 2026-04-19 with the `otto-server` token. Credentials live in `~/.env` as `OTTO_LLM_CLIENT_ID` / `OTTO_LLM_CLIENT_SECRET`.
