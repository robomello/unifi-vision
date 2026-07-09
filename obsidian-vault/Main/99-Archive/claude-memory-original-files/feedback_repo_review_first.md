---
name: Review Repos Before Running
description: Always audit repo contents (README, source, dependencies) before installing or running cloned projects
type: feedback
---

Always thoroughly review a cloned repo BEFORE running npm install or starting it. Check the README, source code, what it actually does, and any red flags.

**Why:** Roberto cloned Open-Higgsfield-AI which turned out to be clickbait/low-value. Wasted time installing 869 packages and running a dev server for something not worth evaluating.

**How to apply:** After cloning any repo, read the README, scan the source for substance (real implementation vs wrapper/placeholder), check dependencies for anything suspicious, and report findings to Roberto BEFORE proceeding with install/run. Let him decide if it's worth continuing.
