---
name: Self-improver overhaul 2026-07-03: LIVE allowlist, score sidecar, backfill
description: Eval/self-improve loop overhaul: minimal LIVE_AGENTS seed chosen without sign-off, sidecar score protocol, state.json backfill applied
type: project
---

Self-improver overhaul landed 2026-07-03 (plan: ~/.claude/plans/self-improver-eval-overhaul.md). Key decisions: (1) LIVE_AGENTS allowlist in config.py seeded MINIMAL read-only only (plan-agent, mechanical-worker, explore-agent, docs-lookup, architect, 4 reviewers) -- Roberto was AFK, did not sign off on the exact list; expanding is a one-line diff, tests/test_live_agents.py forbids mutating agents. (2) Score protocol: improver writes <EVALS_DIR>/last_run.json sidecar (protocol 1), FINAL_SCORE stdout marker is fallback; runner never records 0.0 on parse failure. (3) state.json fake zeros backfilled via backfill_scores.py (6 restored from last-KEPT TSV rows, 3 reset to -1). (4) Known follow-up: verify hooked LIVE agent evals actually produce hook artifacts when the improver runs under claude --print (code-reviewer finding, pre-existing, unverified).
