# Handoff: Agent Flow — Claude Code Pipeline Observer (M1 done)

**Date**: 2026-05-30 15:09:33 (UTC-6)
**Project**: Mello Home Server (`commander/projects/agent-flow/`)
**Branch**: master
**Session Summary**: Built and browser-verified M1 (static UI with mock data) of "Agent Flow", a visual observability layer that renders Claude Code agent runs as a live node-flow — modeled on Jakub Mika's "Fathom → Supabase · pipeline observer" LinkedIn screenshot. Full M2–M4 implementation plan written and file-verified.

## Completed This Session
- **Brainstormed + locked the concept** via the brainstorming skill. Two user decisions captured: (1) first goal = "one real pipeline, live"; (2) data source = **Claude Code hooks, live** (NOT a declared-pipeline SDK). Note: the user's actual intent was clarified mid-session — the reference image is "a flow for *your agent*" (Claude Code itself), so we observe Claude Code runs via hooks; the Fathom pipeline is only the visual reference. (uncommitted — see Git State)
- **Wrote the implementation plan** via plan-agent: `.claude/plans/agent-flow-observer.md` (41KB, carries `<!-- REVIEWED -->`). Grounded in real files (root `docker-compose.yml`, `settings.json`, `.claude/hooks/learning_observer.py`, `claudicle/`). (uncommitted)
- **Ran 3 parallel haiku scouts** that confirmed: hook payload shape, Claudicle telemetry reuse, and house dashboard/Docker/Cloudflare conventions. Findings folded into the plan.
- **Built M1 static UI** (vanilla HTML/CSS/JS, no build step) in `commander/projects/agent-flow/static/`: `index.html`, `styles.css`, `mock-data.js`, `flow.js`, `app.js`. (uncommitted)
- **Verified M1 in browser** (browser-agent, 1460×940): zero console errors. Screenshots saved to `/home/mello/Temp/agentflow_m1_{default,failed,node}.png` (outside repo). Confirmed 3-region layout matches reference: RECENT RUNS sidebar, center node spine (lights-up reveal, same-tool collapse w/ count, subagent nesting, green/red), Run Details panel (OVERVIEW/INPUT/OUTPUT/LOGS + DETAILS + "TIMING IN THE FULL RUN" waterfall).
- Fixed a CSS typo in `styles.css` scrollbar rules (garbled `#1d virtual` / `#2a3span` → valid hex).

## In Progress
- [ ] **Awaiting user decision on sequencing** (asked right before compact, still unanswered): (a, recommended) build M2 live-data now, then deploy; vs (b) deploy M1 mock to `flow.synai.ai` first so it's clickable from anywhere today. Resume by re-asking this.

## Pending (Not Started)
- [ ] **M2 — collector + hooks + live updates**: `app/{models,ingest,reducer,broker,api,main}.py`, SSE `/events`; `hooks/agent_flow_emit.py` (fail-open) + `hooks/install_hooks.py`. First milestone that TOUCHES the live system (installs a hook into `settings.json`).
- [ ] **M3 — storage + replay + details + cost**: `app/{store,cost,phases}.py`; SQLite WAL; wire RIGHT panel tabs + waterfall to real data; cost/tokens from Claudicle ClickHouse (JSONL fallback).
- [ ] **M4 — Docker + Cloudflare + tests**: service block in ROOT `docker-compose.yml` (n8n-net, loopback `127.0.0.1:8062:8062`, Python urllib healthcheck), `flow.synai.ai` route via Cloudflare Zero Trust dashboard, pytest 80%+, Playwright E2E. Use **deploy-agent**.
- [ ] **Phase 0 scouts** (narrow, non-blocking M1; gate M2/M3): Scout-Hooks (capture real `PreToolUse`/`Stop`/`SubagentStop`/`UserPromptSubmit` fixtures → `tests/fixtures/`; find per-call tool id for Pre↔Post pairing + `Agent` parent↔child correlation field), Scout-Cost (exact ClickHouse query + confirm creds reach `claudicle-clickhouse:8123` from n8n-net), Scout-Dashboards (does any house dashboard already use SSE).

## Key Decisions Made
- **Decision**: Data source = Claude Code hooks (live). **Reasoning**: user explicitly chose this over a declared-pipeline emit-SDK; observes the real agent with zero per-project code.
- **Decision**: A "run" = one user turn (`UserPromptSubmit`→`Stop`); session groups runs. **Reasoning**: session-as-run = one giant unreadable graph; a turn maps cleanly to one pipeline execution like the reference.
- **Decision**: Vanilla SVG/HTML/JS, no build step. **Reasoning**: matches house "no heavy frontend" norm; reference layout is simple enough; React Flow rejected (forces Vite/Node build + container bloat).
- **Decision**: SSE for live push (not WebSocket/polling). **Reasoning**: one-way server→browser is exactly the need; survives CF proxy; instant node lighting. CONSTRAINT: forces `uvicorn --workers 1` (in-proc broker can't fan out across workers).
- **Decision**: Reuse Claudicle's ClickHouse for cost/tokens, no second collector. **Reasoning**: Claudicle already ingests Claude OTLP→ClickHouse `otel_logs`; Agent Flow is complementary (live flow view, which Claudicle lacks).
- **Decision**: Fail-open hook emitter (detached `Popen`, ≤400ms, always `exit(0)`, spool-on-failure, `AGENT_FLOW_ENABLED` kill switch). **Reasoning**: a hook must NEVER block/break the user's already hook-heavy session.

## Known Issues
- The loopback verify server (`python3 -m http.server 8919`) reported exit 144 in the task tracker — **harmless**: it was killed on purpose by `pkill` after screenshots. (severity: low)
- Plan references the mock fixture as `mock_runs.json`; M1 actually implements it as `static/mock-data.js` (`window.RUNS`) for no-build simplicity. Reconcile naming in M2 when the stub FastAPI route is added. (severity: low)

## Next Steps (Priority Order)
1. **Re-ask the (a) build-M2 vs (b) deploy-M1-first question** — it's the immediate fork the user was answering when they compacted.
2. **If (a)**: run the 3 Phase-0 scouts in parallel, then build M2 (collector + fail-open hook + SSE) and watch a real run light up.
3. **If (b)**: deploy-agent adds M1 to root compose + `flow.synai.ai` route, then proceed to M2.
4. Commit the uncommitted M1 work (currently nothing in this session is committed).

## Files Actively Being Edited
- `commander/projects/agent-flow/static/index.html` — 3-region layout shell + script includes. Complete for M1.
- `commander/projects/agent-flow/static/styles.css` — full dark theme, badges, chips, node spine, waterfall. Complete for M1 (CSS typo fixed).
- `commander/projects/agent-flow/static/mock-data.js` — 8 sample Claude Code runs (`window.RUNS`); shape mirrors planned collector output. Complete for M1.
- `commander/projects/agent-flow/static/flow.js` — vanilla render helpers (icons, node cards, trigger chips, timing waterfall). Complete for M1.
- `commander/projects/agent-flow/static/app.js` — controller: run selection, replay animation, node selection, tab switching. Complete for M1.
- `.claude/plans/agent-flow-observer.md` — the authoritative M1–M4 plan + verified-facts. Source of truth for next session.

## Context for Next Session
- **READ THE PLAN FIRST**: `.claude/plans/agent-flow-observer.md` has the full architecture, file layout, node-derivation model, and verified infra facts.
- **Verified infra facts** (do not re-guess): services on `n8n-net` (external), loopback binds `127.0.0.1:<port>:<port>`; `cloudflared` is a **token tunnel** (~line 566 of root compose) → routes added in Cloudflare Zero Trust **dashboard**, not a config.yml; planned collector port **8062**; subdomain **flow.synai.ai**.
- **Hook payload shape (confirmed)** from `.claude/hooks/learning_observer.py`: stdin JSON has `session_id`, `tool_name`, `tool_input` (dict: `file_path` for Read/Write/Edit, `command` for Bash, `pattern` for Glob/Grep, `subagent_type`+`description` for the **`Agent`** tool), `tool_output`. PostToolUse uses `tool_output`; reducer should also read `tool_response` defensively. The subagent tool is **`Agent`** (NOT `Task`).
- **Existing hooks are busy**: `settings.json` already wires PreToolUse/PostToolUse(incl `*`→`post_tool_router.sh`, `Write|Edit`/`ExitPlanMode`→`review_plan.sh` 900s consensus)/UserPromptSubmit/SessionStart/SessionEnd/PreCompact. `install_hooks.py` MUST back up, deep-merge (append to matcher arrays), validate, be reversible. Fire-and-forget idiom precedent: `.claude/hooks/post_tool_router.sh` (`timeout 0.5s curl ... &`).
- **Cost source**: Claudicle ClickHouse at `http://claudicle-clickhouse:8123`, db `claude_logs`, table `otel_logs`, `ServiceName='claude-code'`, cost/tokens on `api_request` rows keyed by `LogAttributes['sessionId']`. Creds `CLICKHOUSE_USER/PASSWORD` in `/home/mello/claudicle/.env` (copy to shared `.env`, never hardcode). Subagent JSONL correlation: `…/<session>/subagents/agent-<hash>.jsonl` (`agentId`=hash, `sessionId`=parent), per Claudicle `docs/claude-jsonl-spec.md`.
- **House rules in force**: no Anthropic/OpenAI/Gemini SDK; no localhost in user-facing output (user uses `https://flow.synai.ai`); immutability; small files (<800 ln); no `||` (use `??`); TDD 80%+; Docker deploy = stop && rm && compose up -d (NOT restart), docker cp not heredoc; Python urllib healthcheck on slim images.
- **To re-preview M1**: `python3 -m http.server <port> --bind 127.0.0.1 --directory commander/projects/agent-flow/static`, then browser-agent screenshot (server-side only; loopback fine for verification).
- `.claude/plans/` and `_handoffs/` are exempt from the doc-file-blocker hook; arbitrary `.md`/`.txt` writes elsewhere are blocked.

## Git State
- Branch: master
- Last commit: 1d0b906 "fix(skool-reply): use Python healthcheck instead of curl" (pre-existing, unrelated to this session)
- Uncommitted changes: **yes** — all M1 work is untracked/uncommitted:
  - NEW: `commander/projects/agent-flow/static/{index.html,styles.css,mock-data.js,flow.js,app.js}`
  - NEW: `.claude/plans/agent-flow-observer.md`
  - (also pre-existing repo noise: modified `docker-compose.yml` + many untracked dirs unrelated to this session)
  - Screenshots in `/home/mello/Temp/` are outside the repo.
