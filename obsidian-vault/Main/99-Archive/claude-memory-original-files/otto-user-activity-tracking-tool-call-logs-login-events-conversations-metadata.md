---
name: OTTO User Activity Tracking + Tool Call Logs (login_events + conversations.metadata)
description: OTTO observability features: login_events table (6 auth event sites with fire-and-forget recording), conversations.metadata JSONB for tool call audit trail, /api/admin/activity endpoints with require_admin
type: project
---

# OTTO User Activity Tracking + Tool Call Logs

Two OTTO observability features. Located under `/home/mbot/otto/app/` (Mercedes server). No new pip deps — uses existing asyncpg + FastAPI + Pydantic.

## Feature 1: Login Events Table

### Schema (`_migrate_login_events()` in `database.py`)

```sql
CREATE TABLE IF NOT EXISTS login_events (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(100) NOT NULL,
    event_type VARCHAR(20) NOT NULL,         -- login | logout | token_refresh | login_failed
    auth_method VARCHAR(20) NOT NULL,         -- ldap | local | dev | unknown
    ip_address VARCHAR(45) NOT NULL,
    user_agent VARCHAR(500) DEFAULT '',
    details JSONB,                            -- e.g., {"role": "admin"}
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_login_events_user ON login_events (user_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_login_events_type ON login_events (event_type, created_at DESC);
```

### 6 Auth Event Sites (`app/routers/auth.py`)

| Location (line) | Event Type | Auth Method |
|---|---|---|
| Dev mode success (after 261) | `login` | `dev` |
| LDAP success (after 332) | `login` | `ldap` |
| Local success (after 379) | `login` | `local` |
| Login failure (398, before HTTPException) | `login_failed` | `unknown` |
| Logout (inside 467-471) | `logout` | from token payload |
| Token refresh (after 562) | `token_refresh` | from token payload |

Pattern (fire-and-forget, never blocks auth response):
```python
asyncio.create_task(_safe_record_event(
    user_id=username,
    event_type="login",
    auth_method="ldap",
    ip_address=client_ip,
    user_agent=request.headers.get("user-agent", "")[:500],
    details={"role": role.value},
))
```

`_safe_record_event` catches Exception broadly + logs.warning — never raises into the auth flow.

### Admin Router (`app/routers/admin_activity.py`, prefix `/api/admin`)

- `GET /activity` — filterable (user_id, event_type, from_date, to_date), paginated (limit 1-500 default 100, offset). `require_admin` dep. Returns `{events, total, limit, offset}`.
- `GET /activity/stats?days=N` — aggregate (unique users, events by type, busiest hours). `require_admin`.

Register in `app/main.py` line ~155 next to `server_health_router`.

## Feature 2: Tool Call Logs in Chat

### Schema (`_migrate_conversations_metadata()`)

```sql
ALTER TABLE conversations ADD COLUMN IF NOT EXISTS metadata JSONB;
```

NOT encrypted (contains tool names + timing, no user data). `content` stays human-readable.

### Tool Log Module (`app/memory/tool_log.py`)

- `format_tool_summary(agent_stats)` → human-readable lines:
  ```
  [Tool] get_shift_oee (352ms)
  [Tool] get_stillstand (189ms)
  2 tool calls | 541ms total
  ```
- `build_tool_metadata(agent_stats)` → JSONB:
  ```json
  {"type": "tool_calls", "tools": [{"name": "...", "duration_ms": 352, "status": "success"}],
   "total_tool_calls": 2, "total_duration_ms": 541, "agent": "factory"}
  ```
- `_redact_arguments(args)` strips keys: `password`, `token`, `api_key`, `secret`, `authorization`
- `inject_tool_messages(session_memory, session_id, user_id, agent_stats)` — calls `add_message(role=SYSTEM, content, metadata)` ONLY when `tool_calls > 0` (so direct_llm queries don't pollute history)

### Session Memory Changes (`app/memory/session.py`)

`add_message` gets optional `metadata: Optional[Dict[str, Any]] = None`. Both encrypted and plain-text INSERT paths include the column with `json.dumps(metadata) if metadata else None`.

`get_history` SELECT includes `metadata` column, passes to `ChatMessage` constructor.

### Chat Router Hook Point (`app/routers/chat.py` lines 100-102)

After orchestrator returns, BEFORE storing assistant message:
```python
agent_stats = result.get("agent_stats", {})
if agent_stats.get("tool_calls", 0) > 0:
    await inject_tool_messages(session_memory, session_id, user_id, agent_stats)

# EXISTING: store assistant response
await session_memory.add_message(...)
```

Ordered awaits prevent race between tool message and assistant message insertion.

`get_chat_history` endpoint includes `"metadata": msg.metadata` in returned dicts.

### Schemas (`app/schemas/chat.py`)

```python
class ChatMessage(BaseModel):
    role: MessageRole
    content: str
    timestamp: datetime
    metadata: Optional[Dict[str, Any]] = None   # NEW
```

`MessageRole.SYSTEM = "system"` already existed.

## Security/Review Notes

- All SQL queries use parameterized `$N` placeholders — never string interpolation
- `user_agent` truncated to 500 chars (defends against header injection abuse)
- `metadata` unencrypted while `content` may be encrypted — acceptable since tool names/timing are not sensitive
- System messages inflate `message_count` in session list — acceptable (reflects actual conversation)
- `login_events` growth: needs future retention policy (out of scope now)
- `_redact_arguments` must cover nested dicts
- `from_date`/`to_date` validated as ISO format in admin router
- `ALTER TABLE ADD COLUMN IF NOT EXISTS` is idempotent

## Verification Commands

```bash
# Verify migrations
docker exec mercedes-postgres psql -U otto -d otto -c "\d login_events"
docker exec mercedes-postgres psql -U otto -d otto -c "SELECT column_name FROM information_schema.columns WHERE table_name='conversations' AND column_name='metadata'"

# Test event recording via dev login → admin endpoint
curl -sk -X POST https://53.68.46.101/api/auth/login -d '{"username":"otto-admin","password":"..."}'
curl -sk https://53.68.46.101/api/admin/activity -H "Authorization: Bearer <admin>"

# Test tool-call injection
curl -sk -X POST https://53.68.46.101/api/chat -H "Authorization: Bearer <token>" -d '{"message":"What is the OEE for Final 4?"}'
curl -sk "https://53.68.46.101/api/chat/history/<session-id>" | jq '.messages[] | select(.role=="system")'
```

See [[otto-server]] + [[otto-v2-status-snapshot-2026-04-27]] for OTTO baseline.
