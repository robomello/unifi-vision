---
name: GPU burn-in / resale certification tool
description: Reusable GPU stress-test + per-card PASS/FAIL report harness at ~/gpu-reports/
type: reference
---

`/home/mello/gpu-reports/run-burn.sh <GPU-UUID> "<label>" [minutes]` runs a full burn-in and writes a per-card PASS/FAIL report: identity (VBIOS/UUID/PCIe), full-VRAM pattern test, sustained fp32 SGEMM with per-sample correctness checking under heat, thermals/power/clocks, thermal/HW throttle detection, and PCIe bandwidth. Runs isolated in the `comfyui:local` image (torch+CUDA); auto-stops then restarts any container using the target GPU (trap on EXIT). Harness: `gpu_burn_report.py`; usage in `README.md`. Find UUIDs with `nvidia-smi -L`.

Built 2026-05-30 to certify used GPUs for resale. First run: RTX 3080 Ti (12GB Ampere) PASSED a 60-min soak — 25.9 fp32 TFLOPS, 0 compute errors, 0 VRAM errors, flat 70C, 0 throttles.

Caveat: this server's GPU-0 slot trains at PCIe Gen2 x1 (~0.4 GB/s) — slot/riser limitation, not a card fault; the harness labels it as such and it does not affect the compute/VRAM/thermal cert. Watch out: the system-watcher auto-restarts GPU-0 containers (whisper-stt, ollama-embed) shortly after a manual `docker stop`, so they may resurrect mid-burn (harmless — the burn already owns the VRAM).
