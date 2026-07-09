---
name: Caveman A/B benchmark published as public repo
description: Public repo robomello/caveman-65-percent-myth backing the caveman token-savings audit; reproducible harness + raw JSON, plugin pinned, MIT
type: reference
---

Public GitHub repo backing the [caveman A/B test](#src-reference-caveman-mode-myth): **https://github.com/robomello/caveman-65-percent-myth** (public, MIT, Roberto's copyright).

Published 2026-05-30 to answer a LinkedIn critique (Amr Osama, under his caveman-praise post) that the audit had "no replication steps or a github with your benchmarking steps." Packaged from `/home/mello/commander/projects/caveman-ab-test/`; standalone local clone at `/home/mello/repos/caveman-ab-test/`.

Contents: README (claim-vs-measured + reproduce steps), RESULTS.md + RESULTS_ECOMMERCE.md (original lab notes), raw per-arm JSON in `results/` (session IDs redacted, costs/usage intact), harness (`run_ab.sh`, `run_big.sh`, `compare*.py`, `tasks/`), and `scripts/clone-plugin.sh` pinning JuliusBrussee/caveman @84cc3c14 (referenced, not vendored).

Framing the repo adds on top of the original note: savings split across THREE axes people conflate, output tokens (−8% to −41%), cost in dollars (−2.5% short tasks / −11.9% at scale), and total-token throughput = rate-limit consumption (−26.8% on write-heavy). So "I hit Claude's limits less with caveman" is real on the throughput axis even though the viral 65% cost claim is false. Use this distinction when the 65%/75% caveman claim comes up again.
