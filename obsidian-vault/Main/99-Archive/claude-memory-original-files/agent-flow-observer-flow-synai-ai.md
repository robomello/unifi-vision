---
name: Agent Flow observer (flow.synai.ai)
description: Live Claude Code hook observer: arch, ports, deploy; M1-M4 all done + committed
type: project
---

**Agent Flow** = live node-flow observer of Claude Code's own agent runs (hook events -> SSE -> browser). `/home/mello/commander/projects/agent-flow/` (in the **commander** nested git repo).

**Live:** https://flow.synai.ai (Cloudflare Access -> mello_roberto@hotmail.com + robomello79@gmail.com). Container `agent-flow`, loopback `127.0.0.1:8063`, networks `n8n-net` + `claudicle_default`, in root docker-compose.yml. Tunnel route on token tunnel <REDACTED-UUID-2>.

**Arch:** FastAPI, MUST run `--workers 1` (in-process SSE broker). UI+API+SSE on one port. Endpoints: /healthz /runs /runs/{id}/nodes /runs/{id}/waterfall /events(SSE,no backfill) /ingest(POST,token-gated). run id=`{session_id}#{turn}`.

**Hook:** ~/.claude/hooks/agent_flow_emit.py (fail-open, kill switch AGENT_FLOW_ENABLED). In ~/.claude/settings.json hooks+env. Only NEW sessions/subagents emit. Uninstall: install_hooks.py --uninstall.

**M3 (done):** store.py=SQLite WAL /data/agent-flow.db (survives restart, verified). cost.py=ClickHouse claude_logs.otel_logs api_request rows (cost_usd/input_tokens/output_tokens by session.id), parameterized, 10s cache, fail-safe; verified $7.89 live. claudicle-clickhouse is on claudicle_default (NOT n8n-net) -> agent-flow joins it. phases.py=waterfall(). Creds in /home/mello/claudicle/.env.

**Status:** ALL milestones done, deployed, reviewed, committed. M4 root 9689cf6 / commander 9404b75; M3 commander 4d9f8e2 / root 1f3d9a7. 217 tests green (store/phases 100%, cost 94%, reducer 96%). Future-only: cost cache LRU + batch query if run counts grow.
