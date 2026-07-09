---
name: LTX-2.3 cold loads can trigger system-watcher restart
description: Long initial model loads for LTX-2.3 22B + LoRAs can stall ComfyUI HTTP and get killed by system-watcher; warm up first
type: feedback
---

feedback: When LTX-2.3 22B distilled video runs vanish after 25-30 minutes with empty history and no MP4 output, the system-watcher restarted comfyui because /system_stats health check timed out during long initial model load (22B base + 3 LoRAs + Qwen2.5-VL encoder). Workaround: warm up models with a small T2V run before launching the long I2V/dual-character workflow.

Why: ComfyUI's HTTP server can become unresponsive during cold model load; /home/mello/system-watcher.sh marks comfyui unhealthy and triggers fix_and_restart, which kills the in-progress job and wipes history.

How to apply: Before queuing any new LTX-2.3 22B workflow that has 3+ LoRAs, first queue a 25-frame warmup with the base T2V workflow to get models cached. Or temporarily raise MAX_HEALTH_FAILURES in system-watcher.sh.
