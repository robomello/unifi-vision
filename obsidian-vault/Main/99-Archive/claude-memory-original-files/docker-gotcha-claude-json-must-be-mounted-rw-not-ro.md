---
name: Docker gotcha: .claude.json must be mounted RW (not RO)
description: Mounting .claude.json read-only causes claude CLI to silently return empty output with exit 0.
type: feedback
---

**Rule:** When mounting `~/.claude.json` into a Docker container that runs `claude --print`, mount it **read-write** (no `:ro`). Read-only causes silent failure: empty stdout, empty stderr, exit code 0.

**Why:** Claude CLI refreshes its OAuth token on every invocation and writes the refreshed token back to `.claude.json`. If the file is RO, the refresh fails — and the failure path is silent (no error to stdout/stderr, just empty output). This costs minutes to diagnose because nothing in the container looks wrong.

**How to apply:** In `docker-compose.yml`, every service that calls `claude --print` needs:
```yaml
volumes:
  - /home/mello/.claude:/home/mello/.claude            # rw
  - /home/mello/.claude.json:/home/mello/.claude.json  # rw — NEVER add :ro
```
- `claude-telegram` and `image-telegram` both follow this pattern as of 2026-05-11
- Verified failure mode in `image-telegram` 2026-05-11 14:35–14:41: bot received messages, wrote `(no output)` to every memory row, no error logs. Switching mount from `:ro` to rw fixed it immediately
- The matching CLAUDE.md hint ("Docker gotcha: empty output with exit 0 = check ~/.claude/debug/latest. Fix: mount .claude.json") is correct but didn't specify RW — that's the load-bearing detail
