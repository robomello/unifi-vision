---
name: Genai-Nexus corpintra gateway for Claude (Bedrock Converse API)
description: How OTTO/Mercedes-internal code calls Claude models: genai-nexus.api.corpinter.net Converse-API gateway, NEXUS_API_KEY bearer auth, Bedrock Converse wire shape, confirmed reachable externally
type: reference
---

Corporate AI gateway for Claude access at MBUSI/corpintra: https://genai-nexus.api.corpinter.net/model/<model-id>/converse

Auth: Bearer token via NEXUS_API_KEY env var (not AWS SigV4, not an Anthropic API key) — the gateway handles the Bedrock auth internally.

**Connectivity correction (tested 2026-07-01):** this endpoint is reachable from the public internet, not just from inside corpintra — access control is the bearer token alone, no IP/network restriction observed. Treat NEXUS_API_KEY like any other bearer secret (usable from anywhere if leaked), not as an internal-only credential.

**Confirmed model IDs:**
- Haiku 4.5: `claude-haiku-4-5` (verified live 2026-07-01, HTTP 200)
- Sonnet (unconfirmed version): `claude-sonnet-4` (from earlier example, not independently tested)

Wire format is Bedrock's **Converse API** shape, not Anthropic's native Messages API:
- content is `[{"text": "..."}]`, not a plain string or Anthropic's `{"type": "text", "text": ...}`.
- Response shape: `{"output": {"message": {"content": [...], "role": "assistant"}}, "stopReason": ..., "usage": {...}}` — also Converse-API shaped, not Anthropic's `content`/`stop_reason`/`usage` top-level fields.
- Any code that also talks to Anthropic's API directly needs a translation layer between the two shapes.

Verified working example:
```bash
curl https://genai-nexus.api.corpinter.net/model/claude-haiku-4-5/converse \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $NEXUS_API_KEY" \
  -d '{
    "model": "claude-haiku-4-5",
    "messages": [{"role": "user", "content": [{"text": "Hello, Claude"}]}]
  }'
```
