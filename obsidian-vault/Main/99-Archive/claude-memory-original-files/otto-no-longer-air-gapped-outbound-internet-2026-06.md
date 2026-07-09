---
name: OTTO no longer air-gapped (outbound internet, 2026-06)
description: OTTO now has outbound internet; still not inbound-reachable from the home server (verified 2026-06-18)
type: reference
---

OTTO is **no longer air-gapped** (Roberto confirmed 2026-06-18: "been a while"). It now has **outbound internet**, so on-OTTO `pip install` from PyPI works and runtime egress is possible. This **supersedes** the "air-gapped from public internet" claim in the [OTTO server note](otto-server.md).

Still true (verified from the home server 2026-06-18): the home server **cannot reach into OTTO**. `https://53.68.46.101` and `https://otto.us138.corpintra.net` both return HTTP 000, and the corpintra host does not resolve in DNS here. So OTTO is **outbound-open but not inbound-reachable** from synai.ai infra. Delivery of artifacts (e.g. otto-loop) is still carry-over or an OTTO-initiated pull, not a direct push from the home server.

Implications for otto-loop: offline wheel vendoring is now **optional** (direct `pip install` preferred; keep `vendor/` as a fallback for restricted shells). The model-access policy is unchanged by this (Claude CLI via GenAI Nexus, no SDK) unless Roberto says otherwise.
