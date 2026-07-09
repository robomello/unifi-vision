---
name: OTTO no longer air-gapped (2026-06)
description: OTTO is no longer air-gapped as of 2026-06; otto-loop deploy assumptions (vendoring, GenAI Nexus, delivery) need refresh; home server still can't reach OTTO directly
type: project
---

As of 2026-06-18 Roberto confirmed OTTO (Mercedes-Benz US138 server) is NO LONGER air-gapped ("it's been a while"). The prior memory status (air-gapped from public internet / corporate-intranet only) is OUTDATED — do not rely on it.

Verified 2026-06-18: this home server still cannot reach OTTO directly (curl to https://53.68.46.101 and https://otto.us138.corpintra.net both return 000; no DNS for the corpintra host from here). So 'not air-gapped' means OTTO likely has OUTBOUND internet now, not that the home server has INBOUND reach. Delivery for the otto-loop harness is therefore still carry-over unless a tunnel/VPN is set up.

Implications for the otto-loop harness build (/home/mello/commander/projects/otto-loop): offline pip-wheel vendoring is no longer mandatory (OTTO can pip install directly); re-confirm whether GenAI Nexus is still the model gateway or if model access changed; the rest of the architecture (custom Python harness, OTTO Postgres durability, claude CLI, methodology-not-TensorZero) is unaffected by the air-gap change. Roberto is bringing OTTO's full current architecture for a grounded redesign discussion; refresh the full OTTO memory note once that lands.
