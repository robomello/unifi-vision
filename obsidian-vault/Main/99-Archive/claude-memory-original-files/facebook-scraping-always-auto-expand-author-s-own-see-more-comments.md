---
name: Facebook scraping: always auto-expand author's own See more comments
description: When scraping a FB post, always expand See more on the author's own comments without being asked
type: feedback
---

When scraping a Facebook post (via facebook-scraper-agent), ALWAYS auto-expand every "See more" on comments that belong to the post's author, and pull the full verbatim text, without being asked. Authors routinely put the real payload (the actual prompts, steps, or list bodies) in their own self-reply comment thread, truncated behind "See more," while the caption only holds titles/teasers. Stopping at the titles misses the substance.

**Why:** On the 2026-07-13 "6 Claude prompts" FB group post (share/p/1X392EpTwL), the first scrape returned only the 6 prompt *titles* — the full prompt bodies were behind "See more" in the author's own comments. Roberto had to explicitly ask me to expand them, then made it a standing rule.

**How to apply:** In any FB scrape, after capturing the caption, identify comments authored by the same profile/page as the post, click/expand all their "See more" (and "View more comments" pagination), and return the complete comment text verbatim as part of the default deliverable. Do not summarize or wait for a follow-up request. Non-author comments don't get this treatment by default.
