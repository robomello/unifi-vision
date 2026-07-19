---
name: Memory Capture Auto-Save System
description: Silent auto-capture of repos, videos, status changes into Obsidian via two-stage hook+Haiku classifier
type: project
---

**Signals**: GitHub/video URLs, project-status changes ("we're working on", "drop that"), durable facts/decisions.
**Design**: Stage A = regex gate (fast filter). Stage B = Haiku subprocess classifies & saves via save-memory.py.
**Files**: ~/.claude/hooks/memory_capture.py (UserPromptSubmit), audit at ~/.claude/context/memory-capture.log, backfill via memory_capture_audit.py.
**Integration**: Wire into settings.json UserPromptSubmit.hooks; reuses existing consolidate + memory_sync pipeline.
2026-07-11