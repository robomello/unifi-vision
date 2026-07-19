---
name: RTK Hook Development — 8 Non-Negotiables
description: Durable guardrails for any RTK hook extension work across Claude Code tool surfaces
type: feedback
---

**Always enforce these guardrails for hook work:**
1. Never edit existing `rtk hook claude` Bash block — keep byte-identical
2. All new hooks **fail OPEN** — errors → `exit 0` with no stdout
3. **Never hard-deny Read** — mandatory Read-before-Edit; soft nudge only
4. Keep `settings.json` valid JSON; preserve all pre-existing hooks
5. Backup before edit; use `python3 sqlite3` only (no CLI)
6. Add new hooks as separate PreToolUse blocks, not merged
7. Route through plan-agent consensus (consequential change)
Date: 2026-07-19