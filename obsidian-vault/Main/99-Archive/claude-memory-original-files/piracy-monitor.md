---
name: Piracy Monitor
description: GitHub piracy monitor tool at commander/tools/piracy_monitor/ -- scans for Claude Code piracy repos, scores them, alerts via Telegram, files issues on anthropics/claude-code
type: reference
---

**Location**: `/home/mello/commander/tools/piracy_monitor/` (8 files, zero external deps)

**What it does**: Searches GitHub API (`gh api`) for repos that pirate/bypass Claude Code (proxies, leaked source mirrors, dummy API keys). Scores each repo 0-100 for piracy confidence. Sends Telegram alerts only when an issue is successfully filed on `anthropics/claude-code`.

**CLI** (run from `/home/mello/commander/`):
- `python3 -m tools.piracy_monitor scan` -- full scan + alert
- `python3 -m tools.piracy_monitor test` -- dry run, no alerts
- `python3 -m tools.piracy_monitor status` -- show stats
- `python3 -m tools.piracy_monitor allowlist add owner/repo`

**Cron**: Currently DISABLED (2026-03-31). Was set to */30. Roberto disabled it because community is already mass-reporting the leak repos. Cron entry to re-enable: `*/30 * * * * /home/mello/commander/tools/piracy_monitor/cron_run.sh`

**Context**: Claude Code source was leaked via npm source maps on 2026-03-31. 100+ repos appeared hosting the source. Roberto manually reported `nilupulk/claude-code-free` (anthropics/claude-code#41692), then built this tool to automate monitoring. Auto-filed #41725 as a test.

**Search queries**: 13 queries covering "claude-code-free", "claude code bypass", "claude code proxy", "claude code source", "claude code leaked", sourcemap mirrors, etc.

**Scoring**: Name piracy keywords +30 (max 60), description keywords +20 (max 40), brand+piracy +25, legitimate keywords -30. Classification: piracy >= 60, suspicious 30-59, legitimate < 30.
