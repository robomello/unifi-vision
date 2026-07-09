---
name: Garden bot seasonal reminders
description: Roberto wants garden/plant-care reminders delivered via the garden-telegram bot; reusable cron+docker-exec pattern
type: project
---

Roberto wants garden / seasonal plant-care reminders delivered through the **garden-telegram** bot (his explicit choice on 2026-06-21: "we have the garden telegram, all of these should go there"), not Obsidian or other channels.

Working pattern established 2026-06-21 (first instance: fall lily scaling reminder):
- Sender script lives on the host at `/data/garden-telegram/state/<name>.py`, which is bind-mounted to `/app/data` inside the `garden-telegram` container (source code is baked into the image, so this writable volume avoids an image rebuild).
- The script reads the bot's own `TELEGRAM_GARDEN_TOKEN` and `TELEGRAM_NOTIFICATION_CHAT_ID` from the container env and POSTs to the Telegram sendMessage API via stdlib urllib (no host-side secret handling).
- Invoked by host cron as: `/usr/local/bin/docker exec garden-telegram python /app/data/<name>.py >> /home/mello/logs/garden-reminders.log 2>&1`.
- First instance: `lily_reminder.py`, annual cron `0 9 27 9 *` (Sep 27, 09:00 CT) for fall lily scaling/division. Notification chat id resolved to 1359185565.

Reuse this pattern for any future garden reminders (spring feeding, freeze prep, divide-the-clumps, etc.).
