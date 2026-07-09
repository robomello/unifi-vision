---
name: HTTP 200 is not proof a site is live
description: Automated deploy/liveness checks must visually verify via browser-agent, never trust status code alone — called out for CodeForge Arena redeploy feature
type: feedback
---

Never mark a rebuilt/redeployed benchmark site as "live" based on HTTP 200 alone. A 200 status can come back on a broken page, blank shell, or error page that still returns 200. Must actually load the page with browser-agent and visually confirm real rendered content before showing "deployed"/live status.

Why: Roberto called this out specifically for CodeForge Arena's rebuild-on-demand feature (dead benchmark result links) — reinforcing the existing general rule (agent-behavior.md Rule 5) but in the context of automated redeploy status checks, not just manual UI verification after a code change.

How to apply: any feature that reports a service/site as "up", "deployed", "live", or "working" based on an automated check must use real page-load verification (browser-agent screenshot, or equivalent DOM/content check), never bare HTTP status code checks.
