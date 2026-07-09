---
name: Home GPU layout 2026-06-14: RTX 5090 + RTX PRO 6000 (600W)
description: Verified home-server GPUs: GPU0=RTX 5090 32GB (bus 27, PCIe x1), GPU1=RTX PRO 6000 96GB 600W (bus 29, primary)
type: reference
---

Verified via `nvidia-smi` on the home server on 2026-06-14:

- **GPU 0** (NVML/PCI index 0, bus 27:00.0): NVIDIA GeForce RTX 5090, 32GB GDDR7, 575W default / 600W max. UUID `GPU-a8a771e0`. Slot trains at **PCIe x1** (motherboard slot/bifurcation issue, not the card — current width x1 of x16). Secondary / light tasks only. Never put models >32GB here.
- **GPU 1** (NVML/PCI index 1, bus 29:00.0): NVIDIA RTX PRO 6000 Blackwell Workstation Edition, 96GB, 600W. UUID `GPU-fdfcedb7`. PCIe x16. **PRIMARY** — single-GPU services pin `device_ids: ['1']`.

NVML index order == PCIe bus order (verified, incl. `CUDA_DEVICE_ORDER=PCI_BUS_ID`). So `device_ids: ['1']` = the 96GB PRO 6000, `['0']` = the 32GB RTX 5090.

This CORRECTS two earlier notes:
1. The [baby-otto GPU migration](baby-otto-gpu-migration-both-home-gpus-mercedes.md) plan was to move BOTH home RTX PRO 6000s to Mercedes, leaving home with NO GPU. Actual outcome: only the **Max-Q** PRO 6000 left; the **600W Workstation stayed**, and an RTX 5090 was added in the bus-27 slot. Home KEEPS GPU capability (comfyui, whisper-stt, viqa, street-camera still have GPUs).
2. Supersedes [dual GPU layout restored](dual-gpu-layout-restored-gpu-1-re-added-2026-05-23.md), which described two PRO 6000s (Max-Q + Workstation). The Max-Q is gone.
