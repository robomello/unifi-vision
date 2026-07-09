---
name: Commander Admin Panel — Implementation Plan (memory loss, gallery persistence, identity bleed)
description: Commander web app fixes: load chat history into conversation context (memory bug), persist generated assets to generated_asset table (gallery bug), DB-driven system prompts (identity bleed), CF Access for comfyui/surreal
type: project
---

# Commander Admin Panel — Implementation Plan

Commander web app at `/home/mello/commander/projects/web/` (Next.js 14 + TanStack Query) + agent at `/home/mello/commander/agent.py` + SurrealDB on port 8001 (NS `agents`, DB `commander`). Plan addresses 3 known bugs + security hardening + observability.

## Phase 0 — Security (URGENT)

**Public services without auth**: `comfyui.synai.ai`, `surreal.synai.ai`. Both behind Cloudflare Tunnel already → add Cloudflare Zero Trust Access Application with email OTP policy (Roberto's email).

n8n, Jupyter, NocoDB already have built-in auth — no action.

## Bug #1: Memory Loss Mid-Conversation

**Root cause**: `agent.py::run_agent()` (lines 255-290) creates a fresh conversation array each call:

```python
def run_agent(user_input, model="haiku", max_turns=10):
    conversation = [f"<system>\n{system_prompt}\n</system>"]
    conversation.append(f"\nUser: {user_input}")
```

Chat history from SurrealDB (lines 294-313) is NEVER loaded back into context. `chat()` (318-342) calls `save_chat_message()` but never fetches prior messages.

**Fix in `agent.py:318-342`**: Before invoking the model, query SurrealDB for prior messages in this thread, prepend them to `conversation` as `User:`/`Assistant:` lines.

## Bug #2: Images Not Persisting to Gallery

**Root cause**: Image generation tools in `tools/generation.py` return URLs but do NOT:
1. Save to SurrealDB `generated_asset` table
2. Download to persistent storage
3. Track which thread/conversation generated them

`/api/assets` endpoint (`server.py:1037-1043`) reads from `generated_asset` — but nothing writes to it during generation.

**Fix**:
- `tools/generation.py` — after generation, download the asset to persistent storage AND `INSERT` row into `generated_asset` with `{url, path, prompt, model, thread_id, created_at}`
- `agent.py` — capture tool results so `thread_id` can be threaded through into the asset row

## Bug #3: Identity Confusion (Claude Code context bleeds through)

**Root cause**: `agent.py:158-179` has a hardcoded generic `SYSTEM_PROMPT_TEMPLATE = "You are Commander, Roberto's AI assistant..."`. When using `claude --print`, Claude Code's own context sometimes bleeds through.

**Fix**:
- New SurrealDB table for system prompts (versioned)
- `agent.py` loads active prompt from DB at request time
- Admin Panel page to edit + activate prompts

## Stack Reference

- Backend: FastAPI + `tools/surrealdb_client.py` (async)
- Frontend: Next.js 14 + TanStack Query at `projects/web/`
- DB: SurrealDB :8001
- Agent: text-based at `agent.py`

## Phase Plan (high-level)

| Phase | Scope |
|---|---|
| 0 | Security: CF Access on comfyui + surreal (Cloudflare Dashboard only, no code) |
| 1 | Bug fixes: memory load, asset persistence, system prompt from DB |
| 2-4 | Admin Panel UI: prompt editor, thread browser, asset gallery |
| 5 | Observability: agent run logs, token spend tracking |

PRD reference: `/home/mello/plans/commander-admin-prd.md`. Plan was reviewed and revised with consensus fixes 2026-03-13.

## Why This Matters

Commander is the front door at `cmd.synai.ai` (port 8070). Memory-loss bug makes it feel broken to Roberto every session. Gallery loss means generated images vanish silently. Identity bleed makes responses inconsistent in tone.

See [[active-projects]] for the Commander entry.
