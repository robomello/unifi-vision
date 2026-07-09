---
name: Always use plan-agent, never built-in Plan
description: NEVER use subagent_type="Plan" (built-in). ALWAYS use subagent_type="plan-agent" (custom agent at ~/.claude/agents/plan-agent.md).
type: feedback
---

NEVER use the built-in `subagent_type="Plan"` agent. It exists in the tool list but Roberto's custom `plan-agent` MUST be used instead.

**Why:** Roberto has a custom plan-agent defined at `~/.claude/agents/plan-agent.md` with specific behaviors (writes PLAN.md, includes Team Structure section, triggers consensus review hooks). The built-in Plan agent skips all of this.

**How to apply:** Every time planning work is needed, use `subagent_type="plan-agent"`, never `subagent_type="Plan"`. This is non-negotiable per `~/.claude/rules/planning.md`.
