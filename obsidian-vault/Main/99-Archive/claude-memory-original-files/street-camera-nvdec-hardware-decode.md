---
name: Street Camera NVDEC Hardware Decode
description: street-camera container decodes 4 RTSPS streams (1080p-4K) on GPU 1 NVDEC via ffmpeg+h264_cuvid; CPU dropped 289% to 0.27% while keeping native resolution
type: project
---

The `street-camera` container (project at `/home/mello/commander/projects/street-camera/`) decodes its 4 monitored RTSPS streams on GPU 1's NVDEC silicon engine, not on CPU.

## Architecture
- `rtsp_worker.py` spawns one `ffmpeg` subprocess per camera with `-rtsp_transport tcp -hwaccel cuda -c:v h264_cuvid -i rtsps://... -an -r 5 -f rawvideo -pix_fmt bgr24 pipe:1`.
- Python reads raw bgr24 frames from `proc.stdout`, builds numpy arrays, exposes "latest frame" via `get_latest()` (returns PIL RGB image at native source resolution).
- Codec auto-detected at worker startup via `ffprobe` (default `h264`). `CUVID_BY_CODEC` maps h264→`h264_cuvid`, hevc→`hevc_cuvid`.
- `unifi_client.py` exposes `rtsp_channels[cam_id] = {alias, width, height, fps}` populated from the Protect `/proxy/protect/api/cameras` response (ch0 only, where `isRtspEnabled=true`). Legacy `rtsp_aliases` kept for `get_hires_frame()`.
- `main.py` passes width/height/sample_fps when constructing each `RtspWorker`. `config.SAMPLE_FPS` (default 5) becomes the ffmpeg `-r` flag → only 5 fps reach the Python pipe regardless of source rate.
- `Dockerfile` installs `ffmpeg` via `apt-get` on top of the `ultralytics/ultralytics:latest` base. The NVIDIA Container Toolkit mounts `libnvcuvid.so` automatically because the container has `device_ids: ['1']` + `capabilities: [gpu]` in `docker-compose.yml`.

## Why
- Old `rtsp_worker.py` used `cv2.VideoCapture(url, cv2.CAP_FFMPEG)` which software-decodes H.264. With 4 streams (1920x1080@30, 1600x1200@20, 2688x1512@30, 3840x2160@30 -- ~22 MP/frame combined) it pegged 289% container CPU (~3 cores) for what was supposed to be 5 fps of work.
- The opencv-headless wheel in the ultralytics base has NO CUDA build (`Build info CUDA: False`, `cv2.cudacodec` missing), so OpenCV-side hwaccel was not an option. Subprocess+ffmpeg is the simplest path that works without rebuilding OpenCV.
- `-hwaccel cuda` ALONE does NOT engage NVDEC -- ffmpeg silently picks the software h264 decoder. Must specify `-c:v h264_cuvid` (or `hevc_cuvid`) explicitly. This was verified empirically: the auto-codec path logged "h264 (native)" in ffmpeg info output; the explicit `-c:v h264_cuvid` path uses NVDEC and shows up as a `C` (compute) process bound to GPU 1 in `nvidia-smi pmon`.

## How to apply
- Reading from a Unifi Protect / generic RTSP camera in any future server-side container: prefer this ffmpeg+cuvid subprocess pattern over `cv2.VideoCapture` whenever there's a CUDA-capable GPU available. `libnvcuvid.so` is mounted by the NVIDIA Container Toolkit -- no extra runtime config needed beyond `device_ids` + `capabilities: [gpu]` in compose.
- For codec safety probe with `ffprobe -select_streams v:0 -show_entries stream=codec_name -of default=nw=1:nk=1` (~1s) at worker startup before picking the cuvid decoder.
- NVDEC `dec` column in `nvidia-smi dmon` typically reads 0% even when running -- Blackwell decodes microseconds per frame, rounds to 0 at 1Hz polling. Verify NVDEC is actually engaged by checking that ffmpeg processes appear under `nvidia-smi --query-compute-apps=...` with non-zero `used_gpu_memory`.

## Verification (2026-04-26 night)
| Metric | Before | After |
|---|---|---|
| Container CPU (rolling) | 289% (~3 cores) | 0.27% |
| Container memory | 3.39 GiB | 1.40 GiB |
| GPU 1 VRAM (street-camera) | ~1.5 GB | ~4 GB (4 ffmpeg cuvid contexts ~600 MB each + YOLO 640 MB) |
| GPU 1 power | ~15 W | ~18 W |
| Detection resolution | 4K + 1440p + 1080p (native) | unchanged |

NVDEC on Blackwell can sustain ~8 simultaneous 4K H.264 streams at 60 fps; we use 4 streams at 5 fps -- ~1-2% of capacity. Plenty of room to add the 4 currently-unmonitored cameras (IPD-D53L02-BS, G3 Instant, G4 Pro, Amcrest IP8M-2496E) and/or bump SAMPLE_FPS to 15-30.

## Cameras still available to enable
| Camera | ch0 | RTSP enabled? |
|---|---|---|
| IPD-D53L02-BS | 2592x1944 @ 5fps | yes |
| G3 Instant | 1920x1080 @ 30fps | no -- run `enable_rtsp.py` |
| G4 Pro | 3840x2160 @ 24fps | no -- run `enable_rtsp.py` |
| Amcrest IP8M-2496E | 3840x2160 @ 5fps | yes |

After enabling RTSP where needed, just append camera friendly-names to `config.STREET_CAMERAS` and restart. The NVDEC pipeline picks them up automatically.
