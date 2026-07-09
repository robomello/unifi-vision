---
name: Context-layer pattern for OTTO if it goes multi-user
description: Revisit-when trigger: adopt a context-layer architecture for OTTO only if/when it needs per-user memory + governed data access at scale
type: reference
---

Source: Cole Medin (Redis-sponsored) "I Love the Karpathy LLM Wiki but it Doesn't Scale. Here's What Does." (2026-07-09, https://youtu.be/R-5_2nsF_ZM). Full analysis: /home/mello/commander/projects/youtube-analyses/2026-07-09_cole-medin_karpathy-llm-wiki-doesnt-scale.md

Decision: The personal Obsidian/markdown second brain (my claude-code-memory system) stays as-is — the video's own verdict is that a single-user markdown wiki is ideal; don't change it. Already implement its "promote short-term -> long-term vector memory" pattern via save-memory.py + consolidate-memory.py + the memory_sync cron -> PostgreSQL -> memory-mcp.

OTTO is the ONE thing I ship to other people (5-engineer team, real MBUSI user base), so it's the only system that fits the video's "shipped to production, multi-user" case.

REVISIT-WHEN trigger: if/when OTTO needs per-user memory + governed (access-controlled) data access at scale, adopt the ARCHITECTURE, not the product:
  1. Context layer over a database (not a pile of markdown/files).
  2. Context Retriever = define entities -> auto-generate MCP query tools over business data; access control via scoped agent keys + row-level filters.
  3. Agent Memory = session (short-term) memory + a background pass that extracts durable facts to long-term VECTOR memory, recalled semantically per user.

Constraints: take the pattern, NOT Redis Iris. Iris was in preview and is a cloud dependency that conflicts with the local-first / banned-API posture. Any implementation should be self-hosted (e.g. existing PostgreSQL + pgvector, local embeddings). Production agent framework in the video was Pydantic AI (argued coding-agent SDKs are too slow/token-heavy for shipped agents).

Not needed today: OTTO's current scope does not demand this. This is a dormant trigger, not an action item.
