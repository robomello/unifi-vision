---
name: Caveman Mode Token Savings Myth
description: Audit + own A/B tests debunking viral "75% token savings" claims for Claude Code caveman-mode prompts/plugins. Quality parity confirmed.
type: reference
originSessionId: <REDACTED-UUID-31>
---

## Balázs Turán audit (1.29B tokens, April 2026)

Debunks viral "75% token savings" claims from caveman-mode prompts and Cowork plugin.

Real token distribution in Claude Code:
- Tool results (Read, Grep, file contents): 56%
- Tool use JSON (function calls): 26%
- Claude's chat text: 9%
- System/user messages, images, thinking: 9%

Turán's realistic savings estimate: **3.7% session-wide**, 7% optimistic ceiling.
Cowork sessions (225M tokens): only 2.1% realistic savings.

The "75%" figure comes from simplified benchmarks with no tool use, no file reads,
no conversation history — i.e. not real work.

## Roberto's own A/B tests (2026-04-18, sonnet)

Harness: `/home/mello/commander/projects/caveman-ab-test/`
Plugin loaded per-session via `--plugin-dir`, never installed globally.

### Small single-turn tasks
- explain (pure prose): output -33.8%, cost -0.8%
- review (1 file read + prose): output -40.9%, cost -6.5%
- implement (code-heavy): output -8.2%, cost +1.8%
- **totals across 3 tasks: output -36.9%, cost -2.5%**

Per-session tax: ~600 extra cache_creation tokens from plugin hooks (SessionStart +
UserPromptSubmit injection). Negligible at scale, meaningful on tiny sessions.

### Large multi-turn task (ecommerce MVP scaffold, 21-28 turns)
- TOTAL tokens: 1,578,754 → 1,155,291 (**-26.8%**)
- Cost: $2.06 → $1.81 (**-11.9%**, $0.25 saved)
- Output tokens only dropped 9.1% — most savings came from **cascading cache_read
  reduction (-29.8%)** because smaller per-turn output → smaller accumulated context
  → smaller replay next turn. Compound effect over 22-28 turns.
- Caveman used MORE turns (28 vs 22) but each was smaller. Net win.

### Quality parity (ecommerce scaffold)
Both arms produced all 10 deliverables, all 21 files, all spec-required counts:
- 13 SCHEMA tables, 30 API endpoints, 10 ARCH sections, 50 products, 10/15/12 fixtures,
  6/6 STRIDE categories.
- Products JSON: both have all 14 required fields, identical schema across all 50 items.
- `src/lib/*.ts` files: caveman 20-33% smaller in bytes, NOT from missing features —
  from shorter JSDoc + tighter comments. Function signatures, types, body-algorithm
  comments preserved.
- One notable difference: caveman's auth.ts had 9 functions vs baseline's 11 —
  different decomposition (requireAdmin/requireAuth vs requireRole), not a feature
  gap. Both architecturally valid.
- Ironic: ARCHITECTURE.md was LONGER in caveman (229 vs 185 lines). The prompt
  said "be thorough, do not abbreviate" which overrode caveman rules for deliverables.

**Verdict on quality: equivalent.** Caveman compresses conversation overhead, not
deliverables. Savings come from "thinking out loud" between tool calls, not
content skip.

## Summary of real savings by regime

| Workload | Real cost savings |
|----------|-------------------|
| Small single-turn Q&A | 2-5% |
| Long write-heavy multi-turn session | 10-15% |
| Read/grep-heavy debug session | 3-5% (Turán's regime) |
| Marketing claim | 75% (false) |

## Real token-saving levers for Claude Code (from Turán math)

1. Tighter `head_limit` on Grep output — Grep results are the biggest sink
2. Offload research to subagents — keeps tool results out of main context
3. Read with `offset`/`limit` instead of whole files
4. Prefer Glob/Grep over wide directory reads

## Turán's system-prompt alternative (no plugin needed)

> "Answer directly. Drop pleasantries and preamble. No summaries of what you just
> did. Code blocks and warnings stay formatted and complete."

## Relevance to Roberto

`~/.claude/rules/context.md` already enforces direct communication style, so most
prose-compression gains are already captured. Installing caveman globally would add
~10-15% savings on long write-heavy sessions but costs a ~600-token cache_creation
tax per session. On short interactive sessions the tax can offset savings.

Decision: NOT installed globally. Plugin kept in `caveman-ab-test/caveman-plugin/`
for ad-hoc use via `--plugin-dir` when running long headless scaffolding jobs where
the 10-15% saving is worth it.
