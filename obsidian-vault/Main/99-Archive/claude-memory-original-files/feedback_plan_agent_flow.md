---
name: Plan-agent consensus review is mandatory
description: NEVER bypass the plan-agent's PostToolUse hook (review_plan.sh) - the plan-agent must write PLAN.md itself so Gemini+Codex consensus review fires automatically
type: feedback
---

When using plan-agent, the agent MUST write the plan file itself (not the main session). The plan-agent has a PostToolUse hook on Write|Edit that triggers `~/.claude/hooks/review_plan.sh`, which sends the plan to Gemini and Codex for consensus review.

**Why:** Roberto caught me manually writing the plan file from the main session, which bypassed the consensus review entirely. The hook only fires inside the plan-agent subprocess. Skipping consensus review means the plan goes unvetted by the LLM council.

**How to apply:**
1. When launching plan-agent, tell it to write to PLAN.md (the hook triggers on that write)
2. NEVER manually rewrite the plan file from the main session before the hook has run
3. Wait for plan-agent to return - its response should include reviewer feedback
4. The main session's job is Phase 3 (Final Check): read the consensus-reviewed plan, incorporate feedback, then write the final plan file
5. Only THEN call ExitPlanMode

**Correct flow:**
- Plan-agent writes PLAN.md → hook fires → Gemini+Codex review → plan-agent re-reads and verifies → main session does final check → ExitPlanMode

**Wrong flow (what I did):**
- Plan-agent writes to agent-specific file → I manually rewrite plan file → ExitPlanMode (hook never fired)
