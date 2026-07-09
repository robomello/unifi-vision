---
name: Joey/claude-telegram effort + claude CLI version gotchas
description: Joey effort knob is JOEY_EFFORT (default xhigh); ambient CLAUDE_EFFORT hijacks compose interpolation; claude CLI must be >=2.1.168 for xhigh
type: project
---

**Joey = `claude-telegram`** Docker service (Telegram bot). Runs `claude --print --model claude-opus-4-8 --effort <CLAUDE_EFFORT>` as a full Claude Code agent in `/home/mello`.

**Effort knob:** docker-compose.yml sets `CLAUDE_EFFORT: ${JOEY_EFFORT:-xhigh}` (changed 2026-06-08). It used to be `${CLAUDE_EFFORT:-max}` — but the Claude Code harness exports `CLAUDE_EFFORT=<current session effort>` into ALL subprocesses (including the shell running `docker compose`), so `${CLAUDE_EFFORT:-...}` silently resolved to whatever effort MY interactive session was at, not the intended default. Lesson: never name a service's compose-interpolation var `CLAUDE_EFFORT` (or any var the harness exports) — use a dedicated name like `JOEY_EFFORT`.

**claude CLI version gotcha:** the `xhigh` (Extra High) effort level is REJECTED at runtime by claude-code `2.1.101` ("must be one of: low, medium, high, max") even though `--help` lists it. `2.1.168` accepts it. The container Dockerfile pinned `CLAUDE_CODE_VERSION=2.1.101`; bumped to `2.1.168`. Also: the bot runs `/usr/bin/claude` (image-pinned, non-login `/bin/sh -c`), NOT the host's `/home/mello/.local/bin/claude` (2.1.168) that a login shell would pick up — so `bash -lc 'claude --version'` is MISLEADING for what the bot actually executes. Always test via `sh -c` (non-login).

**Effort levels (ascending):** low, medium, high, xhigh (=Extra High), max.
