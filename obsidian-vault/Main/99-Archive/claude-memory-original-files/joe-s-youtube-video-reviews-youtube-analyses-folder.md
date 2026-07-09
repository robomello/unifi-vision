---
name: Joe's YouTube video reviews (youtube-analyses folder)
description: Joe (claude-telegram bot) writes YouTube video analyses to commander/projects/youtube-analyses/; latest = Nate Herk Fable-5 LLM Wiki
type: reference
---

**What "a video reviewed by Joe" means:** Joe is the `claude-telegram` bot (a Claude Code session over Telegram, tagged `source="joe"` in bot.py). Joe does NOT analyze uploaded video *files* — its `filters.VIDEO` handler just replies "use @Commander_Mello_bot" (bot.py:853). What Joe DOES do: when Roberto sends a YouTube URL, Joe runs the `youtube-analyzer` skill and writes a full analysis markdown to:

`/home/mello/commander/projects/youtube-analyses/YYYY-MM-DD_<channel>_<slug>.md`

To find "the last video Joe reviewed": `ls -lt /home/mello/commander/projects/youtube-analyses/ | head`, or query Postgres `telegram_conversation_memory` (n8n-postgres DB, table stores Joe's chat history) for the most recent assistant message citing that path.

**Last video reviewed (as of 2026-07-05):** "Fable 5 + Karpathy's LLM Wiki is Basically Cheating" — Nate Herk | AI Automation, published 2026-07-03, 14:35, https://youtu.be/hQvwMj7IJe4. Analysis file: `2026-07-03_nate-herk_fable-5-karpathy-llm-wiki.md`.

**The pattern in that video (Karpathy LLM Wiki):** drop sources into `raw/`, agent splits each into cross-linked markdown pages under `wiki/`, maintains `index.md` (TOC) + `log.md` (ingest history), with `CLAUDE.md` holding schema + routing rules. Obsidian is only the front-end viewer. Key points: CLAUDE.md acts as a token-efficient router; Fable is admittedly overkill for ingestion (run ingest on Opus, use Fable only for post-ingest synthesis); flat vs structured is a real choice (flat for homogeneous data like meeting transcripts); it's just portable markdown (works with any agent). This is close to Roberto's own Obsidian memory setup (`claude-code-memory.md` + save-memory.py), minus the auto-ingest-from-sources loop.
