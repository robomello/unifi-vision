---
name: Never assert non-existence without verifying
description: Before claiming something doesn't exist / isn't configured / can't be done / isn't running / isn't installed -- search first. Applies to ALL state claims, not just capabilities.
type: feedback
---

NEVER make a confident negative claim about state without verifying. My mental model of the home server is incomplete (49 agents, 30+ skills, dozens of scripts in commander/tools/, MCP servers, n8n workflows, Docker services, files in many trees). I cannot enumerate it from context.

This applies to ANY claim of non-existence or unavailability, not just "do you have access":

| Negative claim | Verification before answering |
|---|---|
| "I don't have access to X" / "X isn't wired up" | `grep -ril <kw> ~/commander/tools ~/.claude/agents ~/skills` + check `~/docker-compose.yml`, `~/.mcp.json` |
| "There's no agent/tool/skill for Y" | `ls ~/.claude/agents/ ~/skills/` + grep |
| "We don't have a config for Z" | `grep -ril Z ~/ --include='*.yml' --include='*.json' --include='.env*'` |
| "That file doesn't exist" | `ls`, `find`, `Glob` -- don't guess |
| "That service isn't running" | `docker ps`, `systemctl status`, `ss -tlnp` |
| "We haven't built X yet" | grep + check git history (`git log --all --oneline | grep`) |
| "There's no API key for X" | check `.env`, `~/.config/`, secrets stores |

**Why:** On 2026-04-26 Roberto asked if I could control his UniFi switches. I confidently said "no" based on a mental list of tools, then offered 3 ways we *could* add access. He corrected me. A 5-second `grep -ri unifi ~/commander` would have found `commander/tools/unifi.py` immediately. The UniFi case was just the example that exposed the broader behavior -- I do this for any state question.

**How to apply:**
- Before any negative claim, run an actual filesystem/system check (grep, ls, find, ps, systemctl, docker -- whichever fits the claim).
- Before any positive claim too: verify the thing actually does what's being asked. Adjacent capabilities (UniFi Protect ≠ Network, Etsy listings ≠ Etsy ads, OAuth for service A ≠ for service B) are NOT interchangeable.
- If after searching I still find nothing: frame as "I searched X, Y, Z and didn't find it" -- not a flat "no". Signals the search happened, invites correction if I missed a location.
- Enforced by `~/.claude/hooks/capability_check.py` (UserPromptSubmit hook, regex on existence/state questions) and Rule 6 in `~/.claude/rules/agent-behavior.md`.
