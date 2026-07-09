---
name: Tier-discriminating model eval: interacting-bugs codebase + false-premise pushback
description: Current evals don't separate model tiers; designed a harder eval (~$0.10-0.30 API spend) that would
type: reference
---

From eval-design session 2026-07-09: existing quick evals fail to discriminate between model tiers (all tiers pass or all fail). Concrete harder design:

- A ~5-file codebase with an **interacting pair of bugs** — fixing one naively breaks the other's test. Forces cross-file reasoning instead of local patching.
- A task requiring the model to **push back on a false premise** in the prompt.
- Estimated cost ~$0.10-0.30 of API spend per run.

Natural extension of [Caveman A/B benchmark](caveman-a-b-benchmark-published-as-public-repo.md).
