---
name: RTK Full Coverage
description: Extend RTK token-saving coverage from Bash-only to Grep, Glob, Read tool surfaces and CLI agents (gemini, opencode)
type: project
---

**Goal**: Extend RTK token-saving from Bash-only to Grep, Glob, Read tools + CLI agents (gemini, opencode).

**Non-negotiables**: existing Bash hook unchanged, new hooks fail OPEN, Read never hard-denied, settings.json valid.

**Phases**: Phase 0 probe subcommands/hooks/interpreters, Phase 1 backup, then implement Grep/Glob/CLI hooks.

**Status**: PLAN ONLY. Plan file: /home/mello/.claude/plans/rtk-full-coverage.md. Recorded 2026-07-19.