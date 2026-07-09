---
name: git-safety-verify-paths
description: NEVER run git rm or destructive git commands to fix a wrong placement -- verify first, ask before destroying
type: feedback
---

When files are committed to the wrong path, do NOT immediately run `git rm` + re-add in one chained command. That's destructive and can wipe unrelated files.

**Why:** I committed files to `machines/mello-server/` instead of `backups/mello-server/` (after being told the correct path TWICE), then tried to `git rm` them in a chained command without stopping to verify what I was removing. Roberto caught this as dangerous.

**How to apply:**
1. When the user gives an explicit path, USE IT. Don't override with assumptions about repo structure.
2. If files end up in the wrong place, STOP and show the user what you plan to do before any destructive commands.
3. Never chain `git rm` with other commands -- run it alone, verify the result, then proceed.
4. For path corrections: `git mv` is safer than `git rm` + `git add`.
