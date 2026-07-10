---
name: Dream Memory Consolidation Pass
description: /dream command: backup, Haiku analysis, merge/prune archive+manifest, rebuild, diff report
type: reference
---

New /dream command at ~/.claude/commands/dream.md: periodic memory consolidation pass (Nate Herk's Auto Dream adapted to our pipeline). Backs up archive+consolidated note to ~/.claude/backups/dream-<ts>/, Haiku subagent analyzes for duplicates/contradictions/stale (evergreen test: useful in a year?), main agent applies max ~15 merge/prune/rewrite changes to archive files + .manifest.md, re-runs consolidate-memory.py, reports diff. Habits & Feedback and User sections are merge-only, never pruned. Synthesis of Herk's system: Main/50-Reference/nate-herk-second-brain.md
