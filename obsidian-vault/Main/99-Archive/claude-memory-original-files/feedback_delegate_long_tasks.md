---
name: Delegate Long Multi-Step Tasks to Agents
description: For any task with download + setup + run + report across multiple steps, spawn an agent to run it end-to-end instead of driving it turn-by-turn from the main session.
type: feedback
originSessionId: <REDACTED-UUID-1>
---
For tasks like "download this model and test it" — anything that chains: fetch/install → configure → run → report — spawn a general-purpose agent to own the whole flow.

**Why:** Roberto called this out explicitly (2026-04-22). I tried to run a model download + smoke test turn-by-turn in the main session. Each turn boundary dropped momentum: process went zombie between checks, torch wasn't in the container, I stopped at each wall instead of routing around it. Main session has to hand work back to the user between steps; an agent pushes through blockers and delivers one final report.

**How to apply:**
- Trigger: ANY multi-step autonomous task — "download and X", "pull and test", "install and run", "scrape and summarize", "audit and fix", "regenerate content and post", or any sequence of ≥3 dependent ops where intermediate steps aren't interesting to the user
- Action: spawn general-purpose agent with self-contained prompt covering the whole task and acceptance criteria
- Don't: poke around in main session investigating files/dirs when an agent could do the whole audit+action+report in one flight
- Don't: babysit with ScheduleWakeup or turn-by-turn polling
- The agent returns once with the final answer; stream back the summary

**Roberto's framing (2026-04-22):** "With OpenClaw, you can just launch an agent and it will take care of everything. And report when done. This is what I need from you." Default to delegation. The main session is for decisions and user-facing output, not execution.

**Exception:** If the user wants to watch progress live or make decisions mid-flight, stay in the main session.
