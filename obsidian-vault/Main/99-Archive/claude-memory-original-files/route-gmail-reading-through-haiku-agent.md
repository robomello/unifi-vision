---
name: Route Gmail reading through Haiku agent
description: Roberto wants email reading/search delegated to a Haiku-model agent, not done directly in main session
type: feedback
---

When reading/searching/triaging Gmail (search_threads, get_thread, summarizing inbox contents), delegate to the **explore-agent** (Haiku-pinned, `~/.claude/agents/explore-agent.md`) instead of calling the Gmail MCP tools directly in the main Sonnet/Opus session.

Why: Roberto said 'when reading email, send haiku' then confirmed 'it falls to the explorer agent' — email reading is read-only lookup/bandwidth work, the same category explore-agent already owns for codebase investigation ("Delegate ALL read-only... investigation here instead of running Glob/Grep/Read/Bash yourself — runs on Haiku, returns cited findings"). Gmail reading is the mail-account equivalent of that job. Same cost-discipline principle as the separate rule that WebSearch/WebFetch fan-out must go through the haiku-pinned web-explorer agent.

How to apply: for any 'check my email / read this email / what's in my inbox' type request, spawn explore-agent (model haiku) to do the Gmail MCP calls (search_threads, get_thread, list_labels, etc.) and return a synthesized, cited answer, rather than calling mcp__claude_ai_Gmail__* tools directly from the main loop. Only fall back to doing it directly in-session if the user is mid-conversation about a specific thread already open and a fresh agent hand-off would lose context.
