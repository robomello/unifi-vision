---
title: Claude Code Memory — Original Files Archive
created: 2026-04-25
updated: 2026-04-25
tags: [archive, memory, claude-code]
status: archived
---

# Claude Code Memory — Original Files Archive

These 73 `.md` files are the original per-topic Claude Code memory files, archived on 2026-04-25 when the system was migrated to a single consolidated note.

## Authoritative source (going forward)
[[claude-code-memory]] — `/home/mello/obsidian-vault/Main/50-Reference/claude-code-memory.md`

## Query tool (Haiku only, never Opus/Sonnet)
```bash
python3 /home/mello/skills/obsidian/query.py "<your question>"
```

## Consolidation tool (rebuild the single note from these files)
```bash
python3 /home/mello/.claude/scripts/consolidate-memory.py
```
- Reads `.manifest.md` in **this** folder (section/order index; was `MEMORY.md` pre-Phase 4).
- Embeds each linked `<slug>.md` from this folder (frontmatter stripped) under a `#src-<slug>` anchor.
- Writes a draft to `/tmp/claude-code-memory-draft.md`, then publishes to the vault via `/home/mello/skills/obsidian/obsidian_notes.py`.
- To verify nothing is dropped, re-run and check for missing sources:
  ```bash
  python3 /home/mello/.claude/scripts/consolidate-memory.py 2>&1 | grep -iE 'missing|referenced|saved'
  ```
  A clean run reports **0 source files missing**.

**Workflow:** edit `.manifest.md` (add/remove/reorder entries) or the `<slug>.md` files here, then run the consolidator to regenerate `claude-code-memory.md`.

## Backup of record
Full filesystem backup (with hidden state files) lives outside the vault at:
`/home/mello/.claude/backups/memory-20260425-114402/`

Files in this archive folder are content-only copies for Obsidian indexing. The filesystem backup is the canonical recovery point.

## Migration metadata
- **File count:** 73 (excludes the original `MEMORY.md` index, which was kept in place as a stub pointer)
- **Total bytes (sorted-name concat):** 138,944
- **Concatenated SHA256:** `456fc94d5118be2dc62eb27049b1b42d2548c32d5987eae2f9b9a192dff6d94b`
- **Migration date:** 2026-04-25
- **Verified by:** 12/12 Haiku spot-checks (`/home/mello/.claude/backups/memory-20260425-114402/_verification.txt`)

## Why archived rather than deleted
- Backwards link target for any agent/script that referenced individual files
- Audit trail for which fact came from which file
- Safety net during the transition (rollback path: copy back to source dir)

These files are no longer the source of truth. Edit `claude-code-memory.md` (consolidated) or query via `query.py`.
