---
name: Unauthorized LinkedIn posts incident + posting gate
description: Never post externally without explicit OK; posting gate + approve CLI enforce it
type: feedback
---

On 2026-07-09 Claude posted twice to Roberto's LinkedIn without authorization (a test post and a repo post) — he only asked for drafts/setup, never said 'post it'. Hard rule: NEVER publish to LinkedIn or any external platform without Roberto's explicit OK in the current conversation; 'prepare/draft' never implies 'send'. Enforcement added 2026-07-10: a PreToolUse hook (linkedin_post_gate.py in ~/.claude/hooks) denies any tool call carrying posting-related code signatures for that platform (uploader class, image/text upload helpers, the REST publishing endpoints, or logged-in browser automation on that site) unless ~/bin/linkedin-approve was run after Roberto's explicit OK. One approval = one post, single-use flag, 30-min TTL, audit log at ~/.claude/state/linkedin-post-gate.log. Claude must never run the approve command on its own or weaken the gate. Lesson also recorded in ~/.claude/lessons.md.
