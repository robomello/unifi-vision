---
name: OTTO Latency Optimization Plan (3.4s → 2.0-2.4s p50)
description: Four-stage OTTO latency reduction: parallel session bootstrap, PromptLoader fan-out, iPortal in-process cache, fire-and-forget critic with trailing SSE
type: project
---

# OTTO Latency Optimization Plan

Reduce typical KPI-query latency from ~3.4 s to ~2.0–2.4 s (p50). Four ordered changes, lowest risk first. Profile decomposition showed ~1.0 s avoidable per query: 500 ms blocking critic + 30 ms serial DB + 50 ms repeated DB prompt loads + cacheable iPortal hits.

## Where the Time Goes (Baseline)

| Phase | Baseline | Target | Saved |
|---|---|---|---|
| Session setup | 20 ms | <5 ms | 15–30 ms |
| Classification | 100 ms | 100 ms | 0 |
| Tool loop (3 tools) | 2700 ms | 1200–2500 ms | 200–1500 ms (cache hits) |
| Critic | 500 ms | 0 ms (async) | ~500 ms |
| HTML render + persist | 35 ms | 35 ms | 0 |
| **Total p50** | **~3.4 s** | **~2.0–2.4 s** | **1.0 s** |

## Implementation Order (highest confidence first)

| # | Optimization | Gain | Risk | Why ordered first/last |
|---|---|---|---|---|
| 1 | Parallel session setup | 30–50 ms | Low | Pure refactor, identical semantics |
| 2 | PromptLoader fan-out | 50 ms cold, ~0 hot | Low | Cache exists; route more callers through it |
| 3 | iPortal in-process cache | 500–1500 ms on hot keys | Medium | New infra but isolated |
| 4 | Fire-and-forget critic | ~500 ms p50 | Higher | Changes validator contract; SSE protocol bump + frontend coordination |

## 1. Parallel Session Setup

`app/routers/chat.py::_process_chat_request` lines 90–115 do session bootstrap serially: `ensure_session → touch_session → get_history → get_profile_context → get_message_count → (optional) get_or_generate_summary → add_message`.

Refactor:
- **Phase A** (serial, idempotent write): `ensure_session` first — subsequent reads target the same row.
- **Phase B** (parallel via `asyncio.gather`): `get_history`, `get_profile_context`, `get_message_count`, `touch_session`.
- **Phase C** (serial): `summary` depends on count; `add_message` last so the orchestrator sees `history` BEFORE the new user turn.

Pool note: `asyncpg` `min=5/max=25` (`app/memory/database.py`). Four parallel reads × concurrent users stays well within headroom.

## 2. PromptLoader Self-Fallback + Wider Adoption

5-min TTL cache already exists (`app/prompts/loader.py::_cache`); critic uses it. What still hits DB on every call:
- `app/orchestrator/router.py::_execute_direct_llm:432` — `prompts_repo.get_by_name("orchestrator")`
- `app/agents/{rag,ipro,ignition,reasoning}.py` — direct `prompts_repo` use

Move the fallback table into the loader so callers can't drift out of sync with `app/prompts/defaults.py`:
```python
_DEFAULT_BY_NAME = {p["name"]: p["content"] for p in DEFAULT_PROMPTS}
# fallback chain in get(): explicit arg → DEFAULT_PROMPTS → ValueError
```

Admin routes (PATCH/POST/preview in `app/routers/prompts.py`) keep using `prompts_repo` directly — they need uncached reads. Admin route MUST call `prompt_loader.invalidate(name)` after every successful PATCH/POST/DELETE.

## 3. iPortal In-Process Response Cache (single-flight, TTL, LRU)

Today `app/tools/iportal.py` + `iportal_api.py` each open a fresh `httpx.AsyncClient` for every iPortal GET → `https://sdwm0p000445.us138.corpintra.net:1880`. **No** in-process cache. The DB-backed `kpi_cache` table (`app/routers/cache.py`) is only populated by an n8n schedule — live tool calls bypass it.

New file: `app/tools/iportal_cache.py` (~140 lines)
- `IPortalResponseCache(default_ttl=60.0, max_entries=512)` — LRU-bounded TTL cache with **per-key single-flight** (`_inflight: Dict[str, asyncio.Future]`)
- `get_or_fetch(endpoint, params, fetcher, ttl)` — coalesces concurrent fetches; errors propagate to ALL waiters and are NOT cached
- Module-level singleton `iportal_cache`
- Memory bound: 512 × ~30 KB ≈ 15 MB

TTL helper picks per-endpoint TTL:
- `/Shift/GetCurrentShift` → 60 s
- `/KPI/GetKPIList` → 900 s (15 min — static-ish lookup)
- `/Stillstand/`, `/QStop/`, `/KPI/GetWaterfall`, `/KPI/GetPerformanceIndicators` → 30 s if `to_date` includes today, 600 s otherwise
- `/KPI/GetShiftOEE` → 30 s
- default 60 s

Wire into both `IPortalClient._get` and `IPortalAPI.get`. Existing per-tool `httpx.AsyncClient` blocks (`GetShiftOEETool.execute:282`, `GetPerformanceIndicatorsTool.execute:400`, `_current_shift_context:67`) refactor to delegate after the singleton lands.

Observability + manual flush via `app/routers/debug.py`:
- `GET /api/debug/iportal_cache/stats` (admin/engineer)
- `POST /api/debug/iportal_cache/clear` (admin)

## 4. Fire-and-Forget Critic with Trailing SSE

`app/validators/response.py::ResponseValidator.validate` awaits `AnswerCritic.evaluate` (~500 ms via Haiku) **before** returning. Today KPI agent constructs with `fail_on_critic=True` but `agents/kpi.py:619` uses `validated.response if validated.response else content` — so the critic is effectively advisory but still blocks 500 ms.

New `validate_async_critic(...)` returns `(ValidationResult_without_critic, Optional[Task])`. Caller owns task scheduling + lifetime.

KPI agent gated on `settings.critic_async`; `fail_on_critic=False`. Persists verdict to `conversations.response_data->'critic'` via `jsonb_set('{critic}', $1::jsonb, true)` keyed on `decision_id` — column already exists (`_migrate_conversation_rich_reply`).

SSE protocol bump (`/api/chat/stream`):
```
event: progress {...}     # 0+
event: done {...}         # 1 on success
event: quality_check {decision_id, passed, issues, suggestion}  # 0–1, after done
# stream closes within critic_sse_grace_seconds (default 10 s)
```

**Frontend must keep EventSource open after `done`** for up to 10 s. Non-blocking toast on `passed:false`.

### Strong-reference pattern (critical — fix for Python 3.12+ behaviour)

```python
_BACKGROUND_TASKS: set[asyncio.Task] = set()

def _spawn_background(coro) -> asyncio.Task:
    task = asyncio.create_task(coro)
    _BACKGROUND_TASKS.add(task)
    task.add_done_callback(_BACKGROUND_TASKS.discard)
    return task
```

`asyncio.create_task` alone is insufficient — the loop holds only weak refs, GC may eat the task before completion. Don't use bare `asyncio.ensure_future` either.

### Watchdog ordering constraint (load-bearing)

Watchdog MUST be spawned AFTER `add_message` for the assistant turn so the `decision_id` exists in `conversations` when the JSONB merge runs. Otherwise the watchdog writes a row that never gets read.

### Shutdown drain

`app/main.py::shutdown`:
```python
if _BACKGROUND_TASKS:
    try:
        await asyncio.wait_for(asyncio.gather(*_BACKGROUND_TASKS, return_exceptions=True), timeout=5.0)
    except asyncio.TimeoutError:
        for t in _BACKGROUND_TASKS:
            t.cancel()
```

### Config additions (default OFF so it can ship without frontend)

```python
critic_async: bool = False
critic_async_timeout: float = 30.0
critic_sse_grace_seconds: float = 10.0
```

## Verification Checks Worth Keeping

- **Single-flight stress**: 5 concurrent identical queries within 50 ms → `misses=1, hits=4`, exactly one HTTP call to iPortal.
- **No cache poisoning**: simulate iPortal 5xx — error propagates, next call repopulates (errors NOT cached).
- **Critic timeout**: stub `AnswerCritic.evaluate` to `await asyncio.sleep(60)` — SSE closes after 10 s grace, row annotated `critic.timed_out=true`.
- **Container restart mid-critic**: confirm logs show "Draining N background tasks", no exceptions.

## Out of Scope (Explicitly)

- LLM token streaming on `chat_with_tools` (`nexus_client.py` doesn't stream — separate project).
- Replacing asyncpg pool with PgBouncer.
- Reducing KPI agent iteration cap below 10.
- DB-backed iPortal cache (the existing `kpi_cache` table is the n8n pipeline's; this is in-process only).
- KPI agent system-prompt enrichment caching (NocoDB + topology + buffer registry on every call). Track separately if instrumentation shows >50 ms cost.
- Migrating critic to a smaller model (already Haiku).

## References to Get Right

- [Strong refs for free-flying tasks (CPython 91887)](https://github.com/python/cpython/issues/91887)
- [Fire and forget (or never) with Python's asyncio — Michael Kennedy](https://mkennedy.codes/posts/fire-and-forget-or-never-with-python-s-asyncio/)
