---
name: Auto-Reporting Caution
description: Don't auto-spam external issue trackers when community is already handling the problem
type: feedback
---

Before automating mass actions on external platforms (filing issues, DMCA reports, etc.), check whether the community is already handling it.

**Why:** Built piracy_monitor to auto-file issues on anthropics/claude-code every 30 min. Roberto disabled it within minutes because "people are already reporting" the Claude Code source leak. The auto-filing would have been redundant noise on Anthropic's issue tracker.

**How to apply:** When building automation that posts to external repos/platforms:
1. Check if others are already doing it before enabling cron
2. Default to manual/on-demand mode first, only enable auto-mode after confirming it adds value
3. Keep the tool ready but don't fire it automatically unless there's a gap to fill
