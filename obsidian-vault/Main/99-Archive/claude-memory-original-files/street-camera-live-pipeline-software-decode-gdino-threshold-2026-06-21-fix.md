---
name: Street-camera live pipeline: software decode + GDINO threshold (2026-06-21 fix)
description: street-camera RTSP uses software decode (NVDEC cuvid fails on mid-GOP); GDINO MIN_CONFIDENCE=0.25 not 0.45; always verify live detections after changes
type: project
---

The street-camera live pipeline (commander/projects/street-camera) was silently dead ~13 days (06-08 to 06-21): 0 detections, 0 errors, just daily "0 events" reports. Diagnosed + fixed 2026-06-21. Four stacked root causes:

1. **Frame read broken**: rtsp_worker.py used `bufsize=0` + a single `proc.stdout.read(frame_size)`. Pipe reads return PARTIAL data (<=64KB), never a multi-MB frame, so `len != frame_size` broke the loop and no frame ever assembled. Fixed: `bufsize=-1` + a `_read_exactly()` loop.
2. **NVDEC fails in-container**: `h264_cuvid` in the `nvidia/cuda:12.8` image chokes on mid-GOP RTSP joins ("Missing reference picture" -> never outputs a frame, never recovers). Host ffmpeg NVDEC works; the container's does not. Switched to SOFTWARE decode by default; NVDEC is now opt-in via `RTSP_HWACCEL=cuda` (also needs `NVIDIA_DRIVER_CAPABILITIES` to include `video`).
3. **No stall recovery**: ffmpeg reconnect only fired on process exit, not on a hang, so a stalled stream starved the pipeline forever. Added a stall watchdog (`STALL_TIMEOUT_S=30`, kills+reconnects) + a concurrent stderr drain (prevents the stderr pipe filling and blocking ffmpeg).
4. **Threshold too high**: `MIN_CONFIDENCE=0.45` but real GDINO sigmoid scores on these street cams are ~0.25-0.60 (measured: cars 0.25-0.51, a UPS truck at 0.51). Set `GDINO_BOX_THRESHOLD=0.20`, `MIN_CONFIDENCE=0.25`.

LESSON: after ANY street-camera change, verify LIVE detections, not just startup. Check: `docker logs street-camera | grep -E "Saved:|GDINO"`, DB `detections` row count growing, and `nvidia-smi pmon` shows GPU1 python sm% > 0. The "NVDEC/stream open" log fires BEFORE any frame flows, so it is not proof of working. The handoff that introduced this (street-camera-gdino-refactor) listed "verify first live detection" as pending and it was never done.
