---
name: Memory Auto-Capture Hook System
description: Auto-save repos, videos, project-status changes, and decisions to Obsidian via UserPromptSubmit hook without manual invocation
type: project
---

## Goal
Implement UserPromptSubmit hook to auto-capture four signal types (repos, videos, project status, decisions) into correct vault sections silently with audit trail. Close the gap where daily inputs never reach Obsidian.

## Design Status
Phase 0 prerequisites drafted. Three load-bearing facts re-verified in codebase:
- save-memory.py reads body from stdin (no --body flag)
- claude --print --model haiku works detached with --strict-mcp-config --disallowedTools "*"
- UserPromptSubmit payload.prompt field (not --prompt)

Cross-cutting safety: no shell ever (list-form argv + shell=False), explicit worker FDs, recursion guard via env var.

## Next Steps
Run Phase 0 commands before implementation:
1. Verify CLI availability in bare shell
2. Test detached subprocess with no inherited profile
3. Confirm backfill JSONL field shape (user type, message.content shape)
4. Extract manifest section allowlist

Then Phase 1: implement worker + hook integration.

Date: 2026-07-11. Note: message incomplete (cuts at 'MEMORY_CAPTUR').