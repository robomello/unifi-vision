---
name: baby-otto GPU migration (both home GPUs -> Mercedes)
description: 2026-06-14 both home RTX PRO 6000 GPUs move to Mercedes old-OTTO server, renamed baby-otto, for testing
type: project
---

Plan stated 2026-06-13: Roberto is moving BOTH home-server GPUs to Mercedes on 2026-06-14 to test on the old OTTO server, repurposed and renamed **baby-otto**.

Cards: GPU0 = RTX PRO 6000 Blackwell Max-Q (300W TDP), GPU1 = RTX PRO 6000 Blackwell Workstation (600W TDP), 96GB each.

Consequence for home server: loses ALL GPU capability. comfyui, whisper-stt, viqa, street-camera, tts-service go CPU-only or down once the cards are pulled.

Carry-over hardware finding: on the HOME motherboard, GPU0 trained at **PCIe x1** (slot/bifurcation issue, NOT the card; both cards report LnkCap x16/gen5). Re-check `lspci -vvs <bus>` LnkSta width on baby-otto after install. baby-otto needs ~900W of PSU headroom + cooling for the 600W+300W pair.

Capacity findings to re-validate on baby-otto (nemotron-3-super:120b Q4_K_M, 86GB GGUF via Ollama):
- single card decode ~84-90 tok/s; Max-Q ~20% slower than the 600W card (power cap, not PCIe).
- Ollama `num_ctx` is a SHARED KV pool divided across `OLLAMA_NUM_PARALLEL`, hard-capped at the model's native 262144; 150k fits one 96GB card at ~93.6GB.
- 2 separate instances (one model per GPU) = 2x150k @ full speed (135 tok/s aggregate) and beats splitting one model across both (75-78 tok/s shared, 131k/user).
- Bench scripts: /tmp/cc_sweep.sh, cc_thru.sh, cc_split.sh, cc_two.sh; eval project at ~/commander/projects/nemotron-coding-eval.
