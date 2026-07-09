---
name: Best Practices Upgrade
description: 2026-03-30 upgrade -- 49 agent descriptions now trigger-based, 6 agents renamed kebab-case, quarterly maintenance script, agent registry, CLAUDE.md consolidated
type: project
---

# Best Practices Upgrade (2026-03-30)

Reviewed shanraisshan/claude-code-best-practice (GitHub) and "Master Claude Code Skills in 5 Minutes" (craftbettersoftware.com). Applied agent-side improvements only; skills were already in excellent shape (100% trigger descriptions, 100% gotchas, all under 200 lines).

## Changes Made

1. **Agent descriptions**: All 49 agents now have trigger-based descriptions with "Use when...", "Use PROACTIVELY...", "Triggers on...", or "ALWAYS use..." patterns. Previously only 16/49 had them.

2. **Agent naming**: 6 snake_case agents renamed to kebab-case (flux2-agent, kling2pro-agent, nano-banana-agent, seedream-agent, suno-agent, veo3-agent). All cross-references updated in manifest.json, rules/, soul/, claude-ai-skill-bridge.md.

3. **CLAUDE.md consolidated**: Root `/home/mello/CLAUDE.md` is canonical (25 lines). `~/.claude/CLAUDE.md` reduced to a redirect. Updated counts to "49 agents, 20 skills".

4. **Quarterly maintenance**: Script at `~/.claude/scripts/quarterly-maintenance.sh` audits descriptions, naming, duplicates, bloat, CLAUDE.md sync, registry freshness.

5. **Cleanup**: 75 stale todo JSONs archived, 3 duplicate archived agents removed, empty task dirs cleaned.

6. **Settings documented**: Added `_comment` in settings.json explaining bypassPermissions + telegram_confirm.py architecture.

## Pending
- Agent registry (agents/README.md) and rules index (rules/README.md) -- Task #3 in progress.

**Why:** Agent discoverability was poor -- Claude couldn't auto-route to 33 agents with vague descriptions. Naming inconsistency and accumulated bloat were technical debt.

**How to apply:** Future agents MUST have trigger-based descriptions. Run quarterly-maintenance.sh periodically.
