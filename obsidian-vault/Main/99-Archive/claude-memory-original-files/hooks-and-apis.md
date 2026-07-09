---
name: hooks-and-apis
description: Claude Code hooks gotchas -- absolute paths for agents, ExitPlanMode scope, plan review flow, debug log
type: reference
---

# Claude Code Hooks

- **Agent hooks MUST use absolute paths** - `$CLAUDE_PROJECT_DIR` is NOT set for subagents
- **Agent subagents don't trigger ExitPlanMode** - hooks only fire in main session
- **Plan review flow**: `review_plan.sh` single entry point. Called by `post_tool_router.sh`, `review_on_exit_plan.sh`, and plan-agent hook. Saves to `~/.claude/reviews/{timestamp}-{llm}-{plan}.md`.
- **Hook debug log**: `/tmp/claude_hooks.log`
