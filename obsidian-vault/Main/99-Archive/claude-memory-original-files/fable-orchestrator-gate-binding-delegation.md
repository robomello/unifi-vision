---
name: Fable orchestrator gate (binding delegation)
description: Fable main = orchestrator only; PreToolUse gate denies its direct reads/coding, forces delegation
type: feedback
---

Roberto's rule (2026-07-10, after a session where the Fable main thread ran 48 turns with zero delegation): when the MAIN Claude Code session model is Fable (`claude-fable-*`), it is an ORCHESTRATOR ONLY — not a reader, not a coder. It must delegate ALL codebase investigation to explore-agent (Haiku) and ALL coding to Sonnet worker subagents.

Enforcement is now BINDING (advice was ignored). PreToolUse hook `~/.claude/hooks/fable_orchestrator_gate.py` (registered FIRST in settings.json, matcher `Edit|Write|MultiEdit|NotebookEdit|Grep|Glob|Bash`):
- DENY on Fable main thread: Edit/Write/MultiEdit/NotebookEdit, Grep/Glob, and Bash that mutates (`sed -i`, real-file `>`/`>>`, `git commit|add|push|...`, `rm/mv/cp`, `tee`, `chmod`, installs, `docker build/rm/stop`) or investigates (`grep -r`, `rg`, `find -exec`).
- ALLOW: Agent/Task dispatch, single-file Read, read-only orchestration Bash (`ls`, `cat <result>`, `git status/log/diff`, `docker ps`, and `2>/dev/null`/`2>&1`/`>/dev/null` redirects). Opus/Sonnet main sessions and ALL subagents (the delegates) are never gated.
- The gate identifies the main model by tailing the transcript (`transcript_path`) for the most recent `isSidechain=false` assistant `message.model`, enforcing only if it starts with `claude-fable`. Fail-open on any missing signal (never block on uncertainty).

Escape hatch: `~/bin/fable-override --note '<why>'` (single use, 15-min TTL; `--status`, `--revoke`) — only after Roberto's explicit OK. Kill switch: `FABLE_GATE_DISABLED=1`. Audit log: `~/.claude/state/orchestrator-gate.log`. Modeled on the proven `linkedin_post_gate.py`. Supersedes the `explore_agent_nudge.py` nudge when main==Fable (nudge still covers non-Fable sessions).

Bug fixed during verification: the redirect mutation regex originally false-blocked read-only `2>/dev/null`/`2>&1` stderr redirects; corrected to `>>?\s*(?!&)(?!/dev/null)\S` so only real-file writes are denied.
