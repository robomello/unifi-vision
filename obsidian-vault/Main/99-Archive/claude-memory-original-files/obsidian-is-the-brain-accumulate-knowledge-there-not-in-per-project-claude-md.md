---
name: Obsidian is the brain — accumulate knowledge there, not in per-project CLAUDE.md
description: When documenting projects, save to Obsidian first. CLAUDE.md only for narrow load-bearing facts.
type: feedback
---

**Rule:** When writing down what a project IS, how it works, what's where — save it to Obsidian. CLAUDE.md inside a project dir is only for the small set of facts a Claude session needs auto-loaded from cwd.

**Why:** Roberto's memory system is Obsidian (`~/obsidian-vault/Main/50-Reference/claude-code-memory.md`, written via `save-memory.py`, queried via `query.py`). Per-project CLAUDE.md sprawl scatters knowledge across repos and goes stale; Obsidian is one searchable place. Roberto called it "our brain" 2026-05-11.

**How to apply:**
- Comprehensive project docs (architecture, channels, services, status, pipeline) → Obsidian memory entry
- CLAUDE.md in project dir → only when the bot/agent working in that cwd needs facts without round-tripping to Obsidian (e.g. exposed URLs, channel codes, "don't edit X without running Y")
- If both exist, Obsidian is authoritative; CLAUDE.md cites it
- Don't write per-project README docs unless explicitly asked
