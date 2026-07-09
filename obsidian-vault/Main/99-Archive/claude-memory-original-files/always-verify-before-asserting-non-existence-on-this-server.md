---
name: Always verify before asserting non-existence on this server
description: Always grep ~/commander/projects + ~/.claude before claiming a tool/app/agent/skill does not exist on the home server
type: feedback
---

Before claiming any tool/app/skill/agent/file does not exist on this server, ALWAYS run: ls /home/mello/commander/projects/ + grep -ril <kw> in ~/commander, ~/.claude/agents, ~/.claude/skills, ~/skills. The home server has 49+ agents, 30+ skills, dozens of projects in commander/projects/, and Docker services with Cloudflare tunnel routes (e.g. activity.synai.ai -> activity-tracker:8076). Searching obsidian or just one folder is NOT enough.

**Why:** Roberto told me "we created an app to track my daily activity" after I had said no activity tracker existed. I had only checked obsidian and ignored ~/commander/projects/activity-tracker/, which is a real FastAPI app with Postgres backend at port 8076. This wasted his time correcting me.

**How to apply:** Whenever the user mentions "my X", "the Y app/page/tool", or any system component — search broadly across all known plugin/code/service locations BEFORE saying it does not exist. Prefer "I searched A, B, C and did not find it" over a flat "no".
