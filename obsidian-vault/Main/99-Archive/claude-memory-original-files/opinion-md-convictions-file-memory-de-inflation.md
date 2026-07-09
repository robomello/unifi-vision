---
name: opinion.md convictions file + memory de-inflation
description: Claude Code loads ~/opinion.md (Roberto's standing convictions) via @import in ~/CLAUDE.md; created 2026-06-21 and grounded against the Obsidian advisor vault
type: reference
---

On 2026-06-21 we created `/home/mello/opinion.md` — Roberto's standing opinions/convictions, written first-person in his voice so Claude Code knows where he stands before responding. It is grounded against the Obsidian second brain (`00-Advisor/advisor-rules.md`, `mercedes-context.md`, `financial-state.md`, `strategic-decisions-log.md`) and marks each line `[confirmed]` or `[unverified]`. The vault is the source of truth; if opinion.md and the vault disagree, the vault wins.

**Loading:** `~/CLAUDE.md` (project, canonical) has a Session Startup line `@opinion.md` that inlines the file into every session's context. Verified live by probing a fresh `claude --print` session (no tools) — it quoted the file's provenance line back. To change the convictions, edit `~/opinion.md`; the import auto-loads it next session.

**Same session — memory de-inflation:**
- Removed the "8+ businesses, 90+ videos/month" inflation at its source: the identity line in `~/.claude/rules/context.md` (loaded every session) now uses real framing.
- Updated the `Don't inflate Roberto's output` feedback memory to note the source line was corrected.
- Scrubbed the 4 inflated framings inside the `TikTok Shop Victory Plan` memory (90+ videos → ~30; "runs 8 businesses"/"all 8 of my businesses"/"existing 8 businesses" → shops/POD-shops/brands).
- Reconciled the divergent skill count in the two "never assert non-existence" memories to a single number: **30+ skills** (was 20+ and 35+; actual ~31 dirs in `~/skills`, 29 with SKILL.md).

**How to apply:** Memory edits go to the per-file SOURCE in `~/obsidian-vault/Main/99-Archive/claude-memory-original-files/`, then run `python3 ~/.claude/scripts/consolidate-memory.py` to regenerate the read artifact `50-Reference/claude-code-memory.md`. Note still-open inconsistency: agent count appears as both "49 agents" and "49+ agents" — not yet reconciled.
