---
name: Consult Obsidian (2nd Brain) Before Substantive Claims
description: Before asserting what Roberto is doing, has decided, runs in production, or thinks about a topic, search the Obsidian vault first. It's the source of truth; don't contradict it.
type: feedback
originSessionId: <REDACTED-UUID-1>
---
Obsidian vault at `/home/mello/obsidian-vault/Main` (PARA structure) is Roberto's 2nd brain — the durable record of decisions, project state, drafts, research, and opinions. It outranks my inference from CLAUDE.md + MEMORY.md when answering questions about what he's doing or thinks.

**Why:** Roberto called this out explicitly (2026-04-22) after I wrote a Facebook comeback without consulting Obsidian. Quote: "You need to always look at our 2nd Brain. Just to make sure we are not saying that we are not doing." Translation: don't tell him he should do X when his vault already says he decided not to, or claim a project is X when Obsidian has richer context.

**How to apply:**
- Trigger: any substantive answer about projects, stack decisions, drafts, opinions, content strategy, "what have I done on Y", "is this a good idea", or creating copy in his voice
- Action: before answering, run `python3 /home/mello/skills/obsidian/obsidian_notes.py search "<keywords>"` with topic-relevant keywords, then `get` the relevant notes
- Don't: answer from CLAUDE.md/MEMORY.md alone when Obsidian might hold richer context
- Don't: consult Obsidian for trivial ops (reading a log, listing files, git status) — that's overhead without signal

**Skim not exhaustively read:** if search returns 10 notes, read titles/frontmatter first, pull full content only on the 2-3 that look relevant. Don't context-dump.

**When to skip:** direct tool execution, literal code tasks, quick factual lookups the vault wouldn't cover (like "what's the current GPU VRAM"). Use judgment — the rule is about claims regarding Roberto's state/decisions, not every turn.
