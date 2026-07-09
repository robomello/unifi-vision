---
name: Joe Telegram has live web search (joesearch MCP)
description: claude-telegram bot now does live web search via a custom stdio MCP server wired into the Claude CLI
type: project
---

The claude-telegram bot ("Joe") has live internet search as of 2026-06-27. It is NOT limited to its training cutoff anymore.

How it works:
- Custom stdio MCP server: /home/mello/commander/tools/joe_search_mcp.py (self-contained, stdlib + httpx, no langchain). Tools: web_search (Brave), deep_research (Perplexity sonar/sonar-pro), wikipedia, reddit_search. Reads BRAVE_SEARCH_API + PERPLEXITY_KEY from container env.
- Config: /home/mello/commander/tools/joe_mcp_config.json (server name "joesearch").
- Wired into the Claude CLI in claude_runner.py _build_command via `--mcp-config` + `--allowedTools` (mcp__joesearch__* + WebFetch pre-approved, so no Telegram confirm prompt). Constants SEARCH_MCP_CONFIG / SEARCH_ALLOWED_TOOLS at top of claude_runner.py.
- Soul: /home/mello/mello/CAPABILITIES.md has a "Web Search (live internet — USE IT)" section telling Joe to search instead of saying "my cutoff was <date>".

Notes: tools dir is mounted into the container, so the MCP server + config update live without a rebuild; claude_runner.py changes need a `docker compose build` (COPY into image). Only applies to the Claude provider (not the Gemini/Codex paths). Verified live: opus called mcp__joesearch__web_search and returned correct Feb 2026 Super Bowl LX result.
