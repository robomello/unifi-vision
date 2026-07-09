---
name: Telegram feedback for background agents
description: Background scripts should ping Telegram (Commander_Mello_bot, plain text) on milestones; detach via setsid+nohup to survive terminal close
type: feedback
---

For long-running background agents / scripts, send status to Roberto via Telegram (Commander_Mello_bot, env TELEGRAM_CLAUDE_TOKEN, chat env TELEGRAM_NOTIFICATION_CHAT_ID = 1359185565). Plain text (no parse_mode) is safer than Markdown because Markdown breaks on unescaped underscores common in IDs/file paths.

Why: Roberto stated 2026-05-10 'use telegram for agent feedback'. He often closes his terminal mid-run and reads progress on his phone.

How to apply: Background scripts in /home/mello/commander/projects/time-travel-franchise/scripts/* use this pattern:

  source /home/mello/.env
  curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_CLAUDE_TOKEN/sendMessage" \
    -H 'Content-Type: application/json' \
    --data-binary @<(jq -nc --arg c "$TELEGRAM_NOTIFICATION_CHAT_ID" --arg t "$TEXT" '{chat_id:$c,text:$t}')

Detach via 'setsid nohup bash script.sh < /dev/null >> log 2>&1 & disown' so processes survive terminal close. Verify with ps -o pid,ppid,sid,stat — Ss + PPID=1 means immune to SIGHUP.
