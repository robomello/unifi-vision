---
name: Deploy Agent Localhost Fix
description: Always use synai.ai domains instead of localhost URLs for remote access
type: feedback
---

# Deploy Agent - Localhost URL Bug Fix (2026-03-29)

## The Bug
deploy-agent was failing because it was hardcoding localhost URLs in generated configs/commands.

## Root Cause
Roberto accesses the home server **remotely** from his PC. Localhost URLs (`localhost:8070`, `127.0.0.1:8080`, etc.) are unreachable from remote clients. The URLs appear valid in code but fail at runtime when accessed from outside the server.

## Solution
Updated deploy-agent to **always use synai.ai domain names** instead of localhost.

### Domain Mapping Reference
```
Port 8070  → https://cmd.synai.ai (Commander)
Port 8188  → https://comfyui.synai.ai (ComfyUI)
Port 8090  → https://nocodb.synai.ai (NocoDB)
Port 8001  → https://surrealdb.synai.ai (SurrealDB)
Port 5678  → https://n8n.synai.ai (n8n)
Port 9099  → https://arena.synai.ai (CodeForge Arena)
```

## Prevention
- **Golden Rule in CLAUDE.md**: "Server Access -- NO LOCALHOST (NON-NEGOTIABLE)"
- Any agent generating URLs, configs, or commands for remote access must validate against the domain table
- Internal-only services (Whisper STT port 8058, Street Camera Bot port 8098): say "service only accessible server-side"
- If adding new services without subdomains: notify Roberto that Cloudflare Tunnel routes are needed

## Impact
- Fixes deploy-agent output
- Prevents future remote access failures
- Applies to any agent/skill generating URLs for user-facing services
