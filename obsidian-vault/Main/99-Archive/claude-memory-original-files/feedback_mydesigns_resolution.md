---
name: MyDesigns Resolution Facts
description: Nano Banana 2 supports 2K/4K resolution -- don't assume it's 1024-only. Check production code (DreamVault) before claiming engine limitations.
type: feedback
---

Nano Banana 2 (`nano-banana-2`) supports 2K and 4K resolution via MyDesigns API. The DreamVault Telegram bot uses it at 2K in production (`imagegen.py` CLOUD_MODELS config).

**Why:** I incorrectly told Roberto that Nano Banana 2 caps at 1024px based on outdated agent docs, when the actual production bot (dreamvault-gen) was already using it at 2K successfully.

**How to apply:** Before claiming an engine/API doesn't support a feature, check the actual production code (especially Telegram bots like dreamvault-gen) and the API client (`mydesigns_dream.py`). Agent docs can be stale. The code is the source of truth.
