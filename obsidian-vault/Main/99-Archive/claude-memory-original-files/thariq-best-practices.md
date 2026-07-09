---
name: Thariq Best Practices
description: Anthropic's internal skill best practices from Thariq Shihipar's viral post -- 9 categories, description-as-trigger, gotchas sections, progressive disclosure
type: reference
---

# Thariq's Skill Best Practices (Anthropic Internal)

**Source**: [X post by @trq212](https://x.com/trq212/status/2033949937936085378) (Mar 17, 2026, 6.6M views, 44K bookmarks)
**Full extraction**: `/home/mello/x_post_extraction.md`

## 9 Skill Categories

1. Library & API Reference
2. Product Verification
3. Data Fetching & Analysis
4. Business Process & Team Automation
5. Code Scaffolding & Templates
6. Code Quality & Review
7. CI/CD & Deployment
8. Runbooks
9. Infrastructure Operations

## Key Principles

- **Description = trigger condition**, not summary. Include specific phrases + DO NOT exclusions.
- **Gotchas are the highest-signal content** -- built from real failures, updated continuously.
- **Skills are folders** -- use references/, scripts/, assets/ for progressive disclosure.
- **SKILL.md under 200 lines** (target 150). Heavy content goes in reference files.
- **Don't state the obvious** -- focus on what pushes Claude out of defaults.
- **On-demand hooks** -- skills can register session-scoped hooks (e.g., /careful blocks destructive commands).
- **Measure with PreToolUse hooks** -- log skill usage to track adoption.
- **`${CLAUDE_PLUGIN_DATA}`** for persistent data that survives skill upgrades.

## Complementary Resources (added 2026-03-30)

- **shanraisshan/claude-code-best-practice** (GitHub) -- comprehensive reference for agents, commands, skills, orchestration patterns, community workflows
- **craftbettersoftware.com** "Master Claude Code Skills in 5 Minutes" -- three invocation modes (default, manual-only, hidden), scripts over prose, CLAUDE.md should be lean
- **agentskills.io** -- Agent Skills open standard for cross-tool compatibility (Cursor, Gemini CLI, JetBrains, Amp)

## Audit Tool

`skill-auditor` skill created 2026-03-29. Also in `shared/skills/` for OTTO sync.
Runs 9 automated checks: YAML, descriptions, gotchas, progressive disclosure, line counts, reference resolution, duplicates, learnings.md.
