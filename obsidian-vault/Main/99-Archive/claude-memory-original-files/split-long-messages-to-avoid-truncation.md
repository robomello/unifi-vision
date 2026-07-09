---
name: Split long messages to avoid truncation
description: Long replies get truncated on Roberto's relay (Telegram); chunk into numbered parts
type: feedback
---

Roberto reads assistant replies through a channel that truncates long messages. Observed: a 5-item numbered list arrived with only items 1-2; items 3-5 and the closing offer were silently cut off, and he had to ask for the rest. Likely the Telegram relay (~4096 char limit per message).

**Why:** A single long message silently drops its tail on his end. He misses later list items, steps, and offers without knowing they were sent.

**How to apply:** When a reply will be long, split it into multiple sequential messages and state the count up front (e.g. "Part 1/3"). Keep each part well under ~3500 chars. Prefer several short messages over one long block. Most relevant on truncating channels (Telegram); less critical on the desktop CLI.
