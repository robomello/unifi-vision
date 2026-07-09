---
name: Hook failure on critical gate = stop, fix, retry
description: When a hook fails (even "non-blocking") during a critical flow like ExitPlanMode, plan review, or a quality gate, halt immediately, diagnose and fix the root cause, then retry the failed operation. Never let the flow continue past a failed critical-gate hook.
type: feedback
originSessionId: <REDACTED-UUID-15>
---
When a PreToolUse/PostToolUse hook fails during a critical gate — ExitPlanMode, plan review, code-reviewer gate, or anything that is supposed to verify work before proceeding — treat the "non-blocking status code" as a blocker anyway. Halt the current flow, investigate the root cause, fix it in place, and re-run the operation from the failed step.

**Why:** On 2026-04-10, during an Etsy API migration plan, the `pre-edit.sh` PreToolUse hook failed with `/bin/sh: 1: /home/mello/.claude/hooks/pre-edit.sh: not found` because the script had CRLF line endings (the kernel couldn't find the `/bin/bash\r` interpreter, error message was misleading). The flow continued past the failure and ExitPlanMode presented the plan anyway. Roberto rejected the plan because the hook failure meant his safety guardrails (Anthropic SDK blocker, etc.) had not actually been enforced on the Write that persisted the plan file. He wants the harness to behave agentically: detect hook failure → stop → self-repair → retry.

**How to apply:**
1. After any tool call that produces a hook error line in the result (look for `"PreToolUse:" hook error"`, `"PostToolUse:" hook error"`, `"Failed with non-blocking status code"`, `"hook error"`), treat it as a hard stop even though the runtime labeled it non-blocking.
2. Diagnose the root cause (`file <script>` for CRLF, `bash -n <script>` for syntax, `head -1 <script>` for shebang, check executable bit).
3. Fix the root cause in place — don't skip or disable the hook.
4. Retry the exact operation that failed so the hook gets a chance to run cleanly.
5. Only proceed past the gate (present plan, commit, ship) after the hook has actually succeeded once.
6. Critical gates to watch in Roberto's setup: `pre-edit.sh` (SDK blocker), `doc-file-blocker.sh`, `docker-compose-enforcer.sh`, `review_plan.sh` (consensus review), `review_on_exit_plan.sh`, `telegram_confirm.py` (remote approval).

Especially important for Roberto because he runs `bypassPermissions` mode; the hooks ARE the safety layer.
