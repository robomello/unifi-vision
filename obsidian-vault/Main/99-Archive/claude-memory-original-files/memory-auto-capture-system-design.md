---
name: Memory Auto-Capture System Design
description: Automated capture of repos, videos, project-status updates into Obsidian vault via UserPromptSubmit hook with Haiku classifier and deduplication.
type: project
---

## Goal
Auto-save four signal types (repos/GitHub, videos/YouTube, project-status changes, durable decisions) into vault sections as messages arrive, with audit trail and backfill audit.

## Design

### 1. Capture Hook (`~/.claude/hooks/memory_capture.py`, UserPromptSubmit)
- **Stage A (zero-cost gate)**: Regex scans for repo URLs, video URLs, project-status phrases ("we don't need", "we're working on", "drop that", etc.), durable-fact markers
- **Stage B (detached worker on signal)**: Spawns via `subprocess.Popen` with recursive guard `MEMORY_CAPTURE_WORKER=1`
  - Calls Haiku classifier with untrusted-data warning; expects JSON array: `[{save, confidence, section, type, title, description, body}, ...]`
  - Validates section/type against allowlist; caps body at 4 KB
  - Dedupes against manifest before writing
  - Pipes to existing `save-memory.py` (no new write path)
  - Appends audit log: `timestamp | saved|skipped(reason) | section | title | source-session`

### 2. Wire in `~/.claude/settings.json`
Add `memory_capture.py` to `UserPromptSubmit.hooks` array with 3000ms timeout.

### 3. Backfill Audit (`~/.claude/hooks/memory_capture_audit.py`)
Scans 217 recent session transcripts (default 30-day lookback), extracts missed candidates via Stage A signals, dedupes against manifest, writes review file for approval before writing.

## Properties
- Silent when no signals (zero cost); worker detached, no FD leakage
- Reuses save-memory.py, consolidate-memory.py, memory_sync.py
- Audit trail in `~/.claude/context/memory-capture.log`

2026-07-11