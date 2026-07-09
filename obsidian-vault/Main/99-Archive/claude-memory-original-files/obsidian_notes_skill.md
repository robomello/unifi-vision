---
name: Obsidian Notes Skill
description: Use the obsidian skill to persist project content. Vault at /home/mello/obsidian-vault/Main (PARA), skill at /home/mello/skills/obsidian/SKILL.md, CLI at /home/mello/skills/obsidian/obsidian_notes.py.
type: reference
originSessionId: <REDACTED-UUID-30>
---
Obsidian vault is the durable home for project content — post drafts, plans, research, decisions, reference material. When finalizing project work that's worth keeping beyond the current conversation, save it to Obsidian via the skill.

**Skill**: `/home/mello/skills/obsidian/SKILL.md`
**CLI**: `/home/mello/skills/obsidian/obsidian_notes.py` (save / list / search / get)
**Vault**: `/home/mello/obsidian-vault/Main/` (PARA structure)

PARA categories:
- `00-Advisor` — AI/advisor notes
- `10-Projects` — active project write-ups (default)
- `20-People` — contacts
- `30-Daily` — daily notes
- `40-Decisions` — decision records
- `50-Reference` — durable reference material
- `99-Archive` — completed

**How to apply:**
- When Roberto says "save this to Obsidian", "write this up", or finalizes a draft/plan/research — invoke the skill and call the CLI's `save` command.
- When he references prior project notes — use `search` then `get` to retrieve them.
- Default category is `10-Projects` unless content is clearly daily/decision/reference.
- CLI auto-generates YAML frontmatter (title, created, updated, tags, status). Strips any existing frontmatter from input to keep vault consistent.

**Why:** Roberto wants Obsidian to be the single source of truth for durable project content, always discoverable and retrievable across conversations. This keeps memory lean (just the pointer lives in memory) while keeping the actual content structured and navigable in Obsidian.
