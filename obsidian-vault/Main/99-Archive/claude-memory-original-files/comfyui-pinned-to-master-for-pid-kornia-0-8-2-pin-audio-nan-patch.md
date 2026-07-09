---
name: ComfyUI pinned to master for PiD (kornia 0.8.2 pin, audio-nan patch)
description: ComfyUI runs on pinned master (not a release) for NVIDIA PiD super-res; kornia 0.8.2 pinned for LTXVideo; audio-nan patch + rollback image
type: reference
---

On 2026-05-30 ComfyUI was moved from release tag v0.20.1 to a **pinned master branch** (`master-pinned` @ commit `bb560036`) and the Docker image (`comfyui:local`) rebuilt. Reason: the `PiDConditioning` core node + NVIDIA PiD pixel-diffusion super-res (comfy/ldm/pixeldit) is **master-only — not in ANY release tag** (latest tag v0.22.3 lacks it). A normal "Update ComfyUI" that tracks releases will never pull it.

Key facts for future sessions:
- **Rollback**: image `comfyui:v0.20.1-backup` (id f1d5030) = old working v0.20.1. Revert: `docker tag comfyui:v0.20.1-backup comfyui:local && docker compose up -d comfyui` + `git -C ~/ComfyUI checkout v0.20.1`. (Current good baked image after kornia pin: id 9f74cb6.)
- **kornia pinned to 0.8.2** in `~/ComfyUI/Dockerfile` (after ml_dtypes step). kornia 0.8.3 moved `kornia.geometry.transform.pyramid.pad`, breaking `custom_nodes/ComfyUI-LTXVideo` (its requirements.txt pulls kornia unpinned). Satisfies core's `kornia>=0.7.1`.
- **Audio-NaN patch** in `comfy_api/latest/_input_impl/video_types.py` (`torch.nan_to_num(waveform...).clamp(-1,1)` before AudioFrame mux) is a maintained LOCAL patch carried across upgrades via `git stash`. NOT upstream — reapply after every ComfyUI update. Saved diff: `/tmp/comfyui_local_patches_v0.20.1.diff`; stash@{0} also holds it.
- **PiD models**: `~/ComfyUI/models/pid/*.pth` (NVIDIA `model_ema_bf16.pth` renamed to `PiD_<folder>.pth`). ComfyUI has NO `pid` folder registration and PiD is detected by state_dict keys in `comfy/model_detection.py`, so it loads via "Load Diffusion Model" (UNETLoader) from `models/diffusion_models/`. They are exposed there via **RELATIVE symlinks** (`ln -sfn ../pid/X.pth diffusion_models/X.pth`). MUST be relative: container only mounts `~/ComfyUI/models`->`/app/models`, so an ABSOLUTE `/home/mello/...` symlink dangles in-container ("exists but doesn't link anywhere, skipping"). flux2 PiD decode uses existing `models/vae/flux2-vae.safetensors`. Verify model availability by reading the file INSIDE the container, not just `get_filename_list`.
- **2 pre-existing broken custom nodes** (broken on v0.20.1 too, NOT from the update): `VSRFI-ComfyUI` (needs `cupy`, never installed) and `ComfyUI_IndexTTS` (needs `transformers.cache_utils.OffloadedCache`, removed in transformers 5.x). 137 nodes import fine.
