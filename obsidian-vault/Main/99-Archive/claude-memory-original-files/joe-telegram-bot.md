---
name: Joe Telegram Bot
description: Joe (claude-telegram) -- GLM5 approval hook detail, non-obvious config
type: reference
---

## Joe = claude-telegram

- **Project**: `/home/mello/commander/projects/claude-telegram/`
- **Container**: `claude-telegram`
- **GLM5 approval hook**: `~/.claude/hooks/telegram_confirm.py` (PreToolUse) -- autonomously approves/denies dangerous operations. Has a `SAFE_BASH_OVERRIDES` allowlist for docker exec commands.
