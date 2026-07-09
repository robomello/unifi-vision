---
name: Loop Engineering thread (Thedigitalkinggg)
description: Captured 8-part thread framing Loop Engineering as the next prompt-engineering wave; the 5 moves of a loop
type: reference
---

# Loop Engineering — thread by Thedigitalkinggg

Captured 8-part social thread. Frames "Loop Engineering" as the next skill wave, at the same early stage prompt engineering was ~2 years ago. Pairs with [Loop Feature — Self-Paced or Recurring](loop-feature-self-paced-or-recurring.md) — the `/loop` skill is the concrete Claude Code implementation of this idea.

## Core thesis
- Prompting = you in the loop, typing/reading/waiting manually each time.
- Loop Engineering = you build a system that prompts Claude for you. Claude finds its own tasks, works them, checks its own output, runs again. You design the loop once and walk away.
- The shift is "never writing prompts again," not "writing better prompts."
- Claimed signal (June 2026): Boris Cherny (built Claude Code at Anthropic) said publicly "I don't prompt Claude anymore" — builds loops that prompt Claude for him. (Attribution unverified — thread's claim, not confirmed.)

## The 5 moves of a loop (skip any and it breaks)
1. **Discovery** — Claude finds its own tasks instead of waiting for a list.
2. **Handoff** — each task runs in its own space so nothing collides.
3. **Verification** — a second Claude checks the first's work, starting from the assumption it's wrong.
4. **Persistence** — results saved to a file, not left in a disappearing chat.
5. **Scheduling** — automation wakes Claude on a timer. This is what makes it a loop.

## Four common mistakes
- Skip verification (an AI grading its own work always passes it — need an adversarial second step).
- Leave results in the chat (chats vanish — save to file/doc/sheet immediately).
- Make it too complicated (first loop = one task, one output; add complexity after it works).
- No stop condition (a loop with no stopping rule runs forever and costs money).

## Beginner build (non-dev)
Pick a weekly manual task, write every step in plain language, paste into a Claude Project as standing instructions with your context/goals/tone, trigger with one word ("GO"). Repeatable first, automated later.

## Advanced example (content business)
Project instructed to: find trending AI topics each morning, write 3 post ideas for your audience, draft the best in your voice, flag for review, save all to a shared doc. You open one doc, approve one, done.

## How it maps to our stack
The Claude Code `/loop` skill + `ScheduleWakeup` (scheduling), subagents/worktrees (handoff), adversarial verify agents (verification), and file/Obsidian writes (persistence) already cover the 5 moves natively. See [Loop Feature — Self-Paced or Recurring](loop-feature-self-paced-or-recurring.md).
