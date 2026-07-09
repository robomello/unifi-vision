---
name: claudicle
description: Claudicle - self-hosted Claude Code telemetry dashboard (costs, tokens, tools, transcripts) at claudicle.synai.ai
type: reference
---

Self-hosted Claude Code telemetry dashboard (fork of `telepenin/claudicle`). Collects costs, tokens, tool usage, and full session transcripts via OpenTelemetry.

**Source:** `/home/mello/claudicle/`

**Containers (all on localhost bindings):**
- `claudicle-ui` — Next.js dashboard, `127.0.0.1:3003`
- `claudicle-otel` — OTel collector receiving telemetry from Claude Code, `127.0.0.1:4318`
- `claudicle-clickhouse` — event/session storage, `127.0.0.1:8123` + `127.0.0.1:9000`

**Public URL:** `https://claudicle.synai.ai`
- Tunnel ingress: `http://host.docker.internal:3003`
- DNS: proxied CNAME to `<REDACTED-UUID-2>.cfargotunnel.com` (record ID `<REDACTED-HEX32-1>`)
- Access app UUID: `<REDACTED-UUID-6>` (name: "Claudicle Dashboard")
- Access policy ID: `<REDACTED-UUID-7>` — allow-list of one: `robomello79@gmail.com` via Google OAuth IdP

**Scope caveat:** Claudicle only sees telemetry from Claude Code itself. It does NOT monitor other LLM/API traffic leaving the server (Ollama, OpenRouter, kie.ai, Fal.ai, ElevenLabs, Suno, etc.). For broader egress monitoring a LiteLLM proxy or egress sniffer would be needed — not currently installed.

**How to apply:** When Roberto asks to see Claude Code costs/tokens/tool usage/session transcripts, point him at `https://claudicle.synai.ai`. When he asks about monitoring *all* outbound API calls, remember Claudicle is Claude-Code-only and flag the gap.
