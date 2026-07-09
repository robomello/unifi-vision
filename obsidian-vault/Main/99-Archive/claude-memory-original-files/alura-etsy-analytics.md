---
name: Alura Etsy Analytics
description: Alura.io client at /home/mello/commander/tools/alura_client.py. Etsy keyword/product/shop research for POD. Firebase JWT auth, 500 kw/day limit. Agent: alura-agent (Haiku).
type: reference
---

## Alura Etsy Analytics Tool

**Type:** CLI tool + Claude Code agent (NOT a service/container)
**Status:** Active (used for POD niche research)

### Paths
- Agent: /home/mello/.claude/agents/alura-agent.md
- Client: /home/mello/commander/tools/alura_client.py (518 lines)
- Eval: /home/mello/agent-evals/evals/alura-agent-evals.json

### What It Does
Etsy market research client for Alura.io API:
- Keyword research (score, volume, competition)
- Product search with analytics filters
- Shop analysis
- Trending keywords
- Batch keyword research

Used for POD (Print on Demand) niche analysis — finding winning product niches on Etsy by analyzing keyword scores, competing listings, sales volumes, and revenue data.

### Authentication
Firebase JWT from ~/.cookies/alura_io.json (auto-refreshes via Firebase refresh token, 1hr expiry).
- Token cached at ~/.cookies/alura-token.json (55-minute freshness window)
- Firebase API key: <REDACTED-GOOGLE_API_KEY-1> (from app.alura.io)
- API base: https://alura-api-3yk57ena2a-uc.a.run.app/api (keywords), https://alura-products-2-0-3yk57ena2a-uc.a.run.app/api (products)

### Rate Limits (Growth plan)
- 500 keyword/day
- 500 product/day
- 200 shop/day

### POD Analysis Workflow
keyword research -> get listings -> filter physical/non-personalized/$15-40 -> extract patterns -> score

### Gotchas
- If auth fails, Roberto must re-export cookies from browser to ~/.cookies/alura_io.json
- Always filter out personalized items for POD analysis
- Agent model: Haiku
- Async httpx client with auto-refresh on 401

Why: alura was a MISSING SOURCE in consolidated memory. Key POD research tool.

How to apply: When doing Etsy niche research or POD analysis, use alura-agent or alura_client.py directly. Check token freshness before assuming auth failure.
