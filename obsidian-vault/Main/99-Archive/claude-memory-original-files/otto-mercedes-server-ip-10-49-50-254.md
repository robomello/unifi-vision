---
name: OTTO Mercedes server IP = 10.49.50.254
description: Current IP of OTTO (Mercedes W138) server as of 2026-06-20; replaces old 53.68.46.101
type: reference
---

OTTO (Mercedes-Benz W138 Tuscaloosa) server IP is now 10.49.50.254 (as of 2026-06-20).

This replaces the old 53.68.46.101, which is now stale in:
- ~/.claude/rules/testing.md (Playwright target "OTTO v2 at https://53.68.46.101")
- ~/.claude/rules/context.md / agent references
- the otto project CLAUDE.md scp examples (mbot@53.68.46.101)

Remote access context: OTTO remotes into the home server via the otto@mercedes key in ~/.ssh/authorized_keys. The forced command lands interactive logins in /home/mello/otto and auto-starts Claude Code; rsync/scp/git pass through (read+write). If adding a from= source restriction to that key, use from="10.49.50.254".
