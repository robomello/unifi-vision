---
name: Graphify rejected — not a token saver for our setup
description: Skip pitching graphify as a token-savings tool; only useful for one-shot audits
type: feedback
---

Tested graphify (github.com/safishamsi/graphify) on 2026-05-05. Decided NO.

**Why:** Token-savings pitch doesn't apply to our setup.
- graphify indexes a folder via LLM → builds knowledge graph (HTML/Obsidian/JSON)
- Savings only materialize if you'd otherwise dump whole codebases into context
- Claude Code uses grep/glob/Read which are ~free — graph queries don't replace anything we do
- Indexing 30+ skill files = 50-150k tokens one-time; queries save maybe a few k each
- Break-even: dozens of conceptual queries, plus index goes stale on every edit

**When it could be useful (one-shot audits, not daily):**
- Mapping 49 agents to find duplicates/overlap
- commander/projects/ shared-tool map before refactor
- NocoDB tables ↔ n8n workflows ↔ agents documentation map

**Banned path:** `graphify --backend claude` hits api.anthropic.com directly with ANTHROPIC_API_KEY. NEVER use that flag. Default `/graphify` skill mode (Claude Code subagents) would be fine, but we skipped install entirely.

**How to apply:** Don't pitch graphify as a token-saving daily tool. Only suggest it for narrow one-shot audits where the deliverable is a graph diagram, not an ongoing index.
