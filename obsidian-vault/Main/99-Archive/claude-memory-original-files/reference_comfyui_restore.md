---
name: ComfyUI Model Restore Workflow
description: How to re-download ComfyUI models after disk wipes/migrations. Script + inventory + HF API pattern.
type: reference
originSessionId: <REDACTED-UUID-33>
---
**Baseline inventory**: `/home/mello/comfyui-models-inventory.md` (manual snapshot, dated 2026-03-27, 165 files / 955 GB). Keep updating this when major adds/removes happen. **Baseline is a snapshot, not truth** — any model downloaded after the snapshot date won't be in the restore script. Example: `flux.1-dev-SRPO-bf16.safetensors` from `rockerBOO/flux.1-dev-SRPO` was missed on 2026-04-21 restore until user flagged it. Always cross-check inventory against recent downloads when doing a full restore.

**Restore script**: `/home/mello/restore-models.sh` — uses `aria2c -x 16 -s 16 -k 1M -c` with a `fetch(url, subdir, filename)` helper that SKIPs if file already exists. Idempotent, resumable.

**HF API for URL discovery** (when WebFetch/WebSearch unavailable):
```bash
# List files in a repo
curl -s "https://huggingface.co/api/models/{org}/{repo}" | python3 -c "import json,sys;[print(f['rfilename']) for f in json.load(sys.stdin).get('siblings',[])]"

# Search by substring
curl -s "https://huggingface.co/api/models?search={term}&limit=10" | python3 -c "import json,sys;[print(m['modelId']) for m in json.load(sys.stdin)]"

# Get actual LFS size (HEAD content-length is redirect size; x-linked-size is real)
curl -sI -L "https://huggingface.co/.../resolve/main/file.safetensors" | awk 'BEGIN{IGNORECASE=1} /^x-linked-size:/{print $2}'

# Confirm URL works: 206 = partial content (range-request), 200 = ok, 404 = wrong path
curl -o /dev/null -s -L -w "%{http_code}" -r 0-0 "$url"
```

**Precision rule** (user 2026-04-20): Always prefer bf16/fp16 full precision. If a bf16 variant exists on HF, NEVER keep fp8/fp4/Q4/Q8 siblings — swap the fetch URL AND delete the on-disk lower-precision file. Exception: `flux2_dev_fp8mixed.safetensors` — no public ComfyUI-compatible bf16 exists (BFL bf16 is gated behind license agreement).

**Non-obvious repo paths discovered during 2026-04-20 restore**:
- `Comfy-Org/vae-text-encorder-for-flux-klein-9b` (note typo "encorder") — houses flux-klein qwen_3_8b text encoders and flux2-vae
- `Kijai/LTX2.3_comfy` — houses LTX-2.3 transformer-only bf16 variants (distilled, dev, distilled-1.1); Lightricks/LTX-2.3 only publishes the full distilled.safetensors (transformer_only_bf16 there returns 404)
- `Kijai/LTXV2_comfy` — subdirs ARE REQUIRED in URLs. Files live under `text_encoders/` (ltx-2-19b-embeddings_connector_{dev,distill}_bf16.safetensors) and `VAE/` (LTX2_video_vae_bf16.safetensors, LTX2_audio_vae_bf16.safetensors, LTX2_video_vae_old_bf16.safetensors, taeltx_2.safetensors). Root-path fetches return 404.
- Each Lightricks LTX-2-19B IC-LoRA is its own repo: `Lightricks/LTX-2-19b-IC-LoRA-{Detailer,Canny,Depth,Pose,Union}-Control`
- Each LTX-2.3-22B IC-LoRA is its own repo: `Lightricks/LTX-2.3-22b-IC-LoRA-{Union,Motion-Track}-Control` (distinct from 19b)
- Each LTX-2-19B camera control LoRA is its own repo: `Lightricks/LTX-2-19b-LoRA-Camera-Control-{Static,Jib-Up,Jib-Down,Dolly-In,Dolly-Out,Dolly-Left,Dolly-Right}`
- Kandinsky 5 Lite T2V safetensors is under `model/` subdir: `kandinskylab/Kandinsky-5.0-T2V-Lite-sft-5s/model/kandinsky5lite_t2v_sft_5s.safetensors`
- LTX-2 Image2Vid Adapter (community): `MachineDelusions/LTX-2_Image2Video_Adapter_LoRa`
- LTX-2 Squish LoRA (409MB): `ovi054/LTX-2-19b-Squish-LoRA/ltx-2-19b-squish-lora.safetensors`
- Wan 2.2 Lightning 4steps LoRAs: `jrewingwannabe/Wan2.2-Lightning_I2V-A14B-4steps-lora/Wan2.2-Lightning_I2V-A14B-4steps-lora_{HIGH,LOW}_fp16.safetensors`
- Wan 2.1 Fun Camera Control 14B bf16: `alibaba-pai/Wan2.1-Fun-V1.1-14B-Control-Camera/diffusion_pytorch_model.safetensors` (rename on save)
- SUPIR upscaler fp16 pruned: `Kijai/SUPIR_pruned/SUPIR-v0F_fp16.safetensors`
- FLUX.1 Turbo Alpha LoRA (alimama bf16 official): `alimama-creative/FLUX.1-Turbo-Alpha/diffusion_pytorch_model.safetensors` (rename on save)
- InstantID: `InstantX/InstantID/ControlNetModel/diffusion_pytorch_model.safetensors` + `ip-adapter.bin` at repo root
- DWPose torchscript: yolox at `hr16/yolox-onnx/yolox_l.torchscript.pt` (not hr16/DWPose-TorchScript-BatchSize5, which only has dw-ll_ucoco_384_bs5.torchscript.pt)
- IP-Adapter clip_vision_vit_h: `h94/IP-Adapter/models/image_encoder/model.safetensors`
- Skin diff detail upscaler: `gemasai/x1_ITF_SkinDiffDetail_Lite_v1/x1_ITF_SkinDiffDetail_Lite_v1.pth` (not Kim2091)
- Qwen 2.5 VL 7B fp8_scaled: `Comfy-Org/HunyuanVideo_1.5_repackaged/split_files/text_encoders/`
- FLUX.2-dev single-file bf16: `black-forest-labs/FLUX.2-dev/flux2-dev.safetensors` is **gated** (401). `Comfy-Org/flux2-dev` only publishes fp8mixed. Keep existing fp8mixed on disk.
- FLUX.2-klein-4B: `black-forest-labs/FLUX.2-klein-4B/flux-2-klein-4b.safetensors` is **ungated** (206)
- `Comfy-Org/ltx-2/split_files/text_encoders/gemma_3_12B_it.safetensors` — 22.7GB bf16 gemma 12B full precision. Use this; symlink `gemma_3_12B_it_fp4_mixed.safetensors` and `comfy_gemma_3_12B_it.safetensors` → bf16 for workflows that hardcode those names.
- `numz/SeedVR2_comfyUI/resolve/main/seedvr2_ema_{3b,7b,7b_sharp}_fp16.safetensors` — fp16 SeedVR2 variants (6.3/15.3/15.3 GB)
- `unsloth/LTX-2.3-GGUF/resolve/main/text_encoders/ltx-2.3-22b-distilled_embeddings_connectors.safetensors` + `vae/ltx-2.3-22b-distilled_{audio,video}_vae.safetensors` — bf16 LTX-2.3 22b VAEs + connectors (2.3/0.4/1.4 GB)
- `okaris/zoe-depth-controlnet-xl/resolve/main/diffusion_pytorch_model.safetensors` — 5GB Zoe Depth SDXL ControlNet (rename on save to `depth-zoe-xl-v1.0-controlnet.safetensors`)
- `Kijai/vitpose_comfy/resolve/main/onnx/vitpose_h_wholebody_{model.onnx,data.bin}` — ONNX external-data pattern: tiny model.onnx (420KB metadata) + 2.4GB data.bin (weights). BOTH required, side-by-side in same dir.
- `Comfy-Org/ACE-Step_ComfyUI_repackaged/resolve/main/all_in_one/ace_step_v1_3.5b.safetensors` — 7.2GB audio gen checkpoint
- `Wuli-art/Qwen-Image-2512-Turbo-LoRA/.../V3.0-bf16.safetensors` is V3 (latest, 1.1GB); -2-Steps repo has V1.0-bf16 (2.2GB, different file)
- `Raspberry-ai/aidmaRealisticSkin-FLUX-v0.1/resolve/main/aidmaRealisticSkin-FLUX-v0.1.safetensors` — 76MB Flux skin LoRA
- `lovis93/next-scene-qwen-image-lora-2509/resolve/main/next-scene_lora_{v1-3000.safetensors,v2-3000.safetensors}` — note inconsistent dash: v1 uses underscore (`_v1-3000`), v2 uses dash (`-v2-3000`)

**Phase 7 (baseline inventory gaps, HF-available, added 2026-04-20)**:
- `DavidHoa/buffalo_l` — InsightFace buffalo_l set (det_10g/1k3d68/2d106det/genderage/w600k_r50.onnx). Target: `insightface/models/buffalo_l/`. Deepinsight official repo is 401, this is the working mirror.
- `DavidHoa/antelopev2` — InsightFace antelopev2 set. NOTE different structure than buffalo_l: uses `scrfd_10g_bnkps.onnx` (not det_10g) and `glintr100.onnx` (not w600k_r50), plus shared 1k3d68/2d106det/genderage. If inventory lists `antelopev2/det_10g.onnx`, that was a buffalo_l file miscopied — the canonical set does not include det_10g.
- `Kijai/LivePortrait_safetensors` — all 6 files at repo root for human set (appearance_feature_extractor/motion_extractor/spade_generator/warping_module/stitching_retargeting_module.safetensors + landmark.onnx). Also has `animal/` subdir with matching set. Target: `liveportrait/` with symlinks into `liveportrait_models/` and `liveportrait_models/human/`.
- `camenduru/facexlib` — `detection_Resnet50_Final.pth` (110MB) + `parsing_parsenet.pth` (85MB). Target: `facedetection/`.
- `madebyollin/taef1/diffusion_pytorch_model.safetensors` (9.8MB) — save as `taef1_decoder.pth` in `vae_approx/`.
- `Kijai/LTXV2_comfy/VAE/taeltx_2.safetensors` (22MB) — LTX-2 TAE latent previewer. Target: `vae_approx/`.
- `stabilityai/stable-cascade/stage_b_bf16.safetensors` (3.1GB) — bf16, use instead of fp32 baseline. Target: `checkpoints/`.
- `Kijai/MelBandRoFormer_comfy/MelBandRoformer_fp32.safetensors` (913MB) — vocal isolation audio model. Target: `audio/`. Original `KimberleyJensen/Mel-Band-Roformer-Vocal-Model` is 401.
- `Osrivers/Wan2.1_VAE_upscale2x_imageonly_real_v1.safetensors` (508MB) — community-mirrored checkpoint filename IS the repo name. Target: `vae/`.
- `hlky/Z-Image-Turbo-Fun-Controlnet-Union-2.1/diffusion_pytorch_model.safetensors` (6.7GB) — Z-Image 2.1 ControlNet Union. Official `alibaba-pai/Z-Image-Turbo-Fun-Controlnet-Union-2.1` is 401.

**Precision-rule skips (low-precision variants NOT restored because bf16/fp16 already present)**:
- `t5xxl_fp8_e4m3fn.safetensors` (have t5xxl_fp16)
- `qwen_image_2512_fp8_e4m3fn.safetensors` (have qwen_image_2512_bf16)
- `seedvr2_ema_3b_fp8_e4m3fn.safetensors`, `seedvr2_ema_7b_fp8_e4m3fn_mixed_block35_fp16.safetensors` (have fp16)
- `qwen_3_8b_fp8mixed.safetensors`, `Flux2Klein/qwen_3_8b_fp8mixed.safetensors` (have qwen_3_8b bf16)
- `ltx-2.3-22b-dev-fp8.safetensors` (have ltx-2.3-22b-dev bf16)
- `gemma_3_12B_it_fp4_mixed.safetensors` (have gemma_3_12B_it bf16, symlinked)
- `jibMixQwen_v50_fp8.safetensors` (4KB broken + fp8)
- `LTX2/ltx-2-19b-distilled-lora_resized_dynamic_fro09_avg_rank_175_fp8.safetensors` (fp8 resized LoRA, custom compression)

**Gated / unavailable**:
- `facebook/sam3/sam3.pt` — returns 401 (gated). Use ONNX version from `wkentaro/sam3-onnx-models` or the existing `sam3.safetensors`.
- `alibaba-pai/Z-Image-Turbo-Fun-Controlnet-Union-2.1` — 401. Use `hlky/` mirror instead.
- `Qwen2.5_7B_instruct_bf16.safetensors` (15GB single-file) — no consolidated HF source (only sharded at Qwen/Qwen2.5-7B-Instruct).
- `StefanFalkok/Wan_2.2_I2V_SVI_2_PRO_8steps` — only has fp8 variants, no fp16 matching baseline filename pattern.
- `flux-2-klein-base-9b-fp8.safetensors` — no bf16 equivalent on HF.

**Civitai-sourced (no HF URL)**: cyberrealisticPony, juggernautXL, turbovisionxl, realvisxlV50, epicrealismXL, invictusredmondStable, ultrarealFineTune, zEpicrealism_turboV1, DasiwaWAN22I2V14BLightspeed, 1GIRL_QWEN_V3, NSFW loras (nsfw_v10, NSFW_master_ZIT, nsfw_wan_umt5-xxl_bf16, nsfw nude group girls), ZIT face loras (EllaPurnell/MadelynCline/ScarlettJohansson/VeronicaRodriguez/fdpo_v1), Samsung/AlanaCho, Qwen-Image_SmartphoneSnapshotPhotoReality_v4, add-detail-xl, skin_4-000015, skin texture Photorealistic style v4.5, BouncyWalk/BounceLow/BounceHigh Wan2_2, date-coded LoRAs (20251206/11/14). Total ~80-100 items. Use CIVITAI_API_TOKEN in `/home/mello/.env` for batch. Internal Klein consistency LoRAs (f2k_consist_20260225, bfs_head_v1_flux-klein_9b, Flux2-Klein-9B-Consistency, Klein-consistency, lenovo_flux_klein9b, flux-klein-tryon-comfy) likely live on an internal drive, not HF.

**Log location**: `/home/mello/restore-models.log`

**Civitai restore pattern (added 2026-04-21)**:
- Token: `CIVITAI_API_TOKEN` in `/home/mello/.env` (query param, NOT Authorization header)
- Download URL: `https://civitai.com/api/download/models/{versionId}?token=$CIVITAI_API_TOKEN`
- Model metadata: `https://civitai.com/api/v1/models/{modelId}` → `modelVersions[].id` + `files[].name`
- **aria2c FAILS on Civitai (rc=22/24) even with correct URL** — Civitai's CF redirect chain has something aria2-incompatible. **Use `curl -sS -L --retry 3 --retry-delay 5`** instead (confirmed working on 6.7GB+ files in 2026-04-21 restore).
- Civitai search API is UNRELIABLE: `?query=<name>` mostly returns trending/recent uploads, not name-match. Resolve by direct `modelId` from old session tool-results or Civitai URL bookmarks.
- Early-access LoRAs return HTTP 401 even with valid token: check `earlyAccessTimeFrame` field in model-version JSON. Internal Klein consistency LoRA `f2k_9B_lcs_consist_20260415` (modelId=1939453) was early-access-gated until 2026-05-01.
- Scripts: `/home/mello/civitai-batch.sh`, `civitai-batch-2.sh`, `civitai-batch-3.sh`, `civitai-parse.py`, log at `/home/mello/civitai-batch.log`
- 2026-04-21 restore manifest (9 items, ~56GB):
  | modelId | versionId | filename | size | subdir |
  |---|---|---|---|---|
  | 277058 | 1920523 | epicrealismXL_vxviiCrystalclear.safetensors | 6.5GB | checkpoints |
  | 2305301 | 2593828 | zEpicrealism_turboV1Fp8.safetensors | 5.8GB | checkpoints |
  | 978314 | 1413133 | ultrarealFineTune_v4.safetensors | 23GB | checkpoints |
  | 827184 | 1761560 | waiIllustriousSDXL_v140.safetensors | 6.5GB | checkpoints |
  | 133005 | 1759168 | juggernautXL_ragnarokBy.safetensors | 6.7GB | checkpoints |
  | 133005 | 920957 | juggernautXL_juggXILightningByRD.safetensors | 6.7GB | checkpoints |
  | 248951 | 340833 | skin_4-000015.safetensors | 218MB | loras |
  | 580857 | 2709995 | skin texture style zib v1.1.safetensors | 163MB | loras |
  | 2168935 | 2442479 | zImageTurbo_vae.safetensors | 320MB | vae |
- Still deferred / unrestorable:
  - Klein consistency LoRAs (f2k_consist, bfs_head, Flux2-Klein-9B-Consistency, etc.) — some are Civitai early-access, most likely internal/not on Civitai
  - Other baseline inventory items (face LoRAs, date-coded test LoRAs, NSFW LoRAs) — no direct URLs, blind search returns garbage. Need manual URL curation if needed.
