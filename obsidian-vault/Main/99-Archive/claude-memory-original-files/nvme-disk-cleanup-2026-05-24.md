---
name: NVMe Disk Cleanup 2026-05-24
description: Cleanup pass on the 3.6T NVMe: freed 348G, removed eplan-win VM and stemdeck-untouched. Notes remaining big consumers.
type: reference
---

# NVMe Disk Cleanup — 2026-05-24

**Drive**: `/dev/nvme0n1p2` (3.6T root).
**Result**: 94% → 83% used. **Freed ~348G total** (244G → 592G available).

## Removed this session

### 1. EPLAN Windows VM (`eplan-win` compose project) — ~73G
- Container `eplan-windows` (dockurr/windows, was running unhealthy)
- Volume `eplan-win_windows-data` (48G)
- Image `dockurr/windows:latest` (382M)
- Network `eplan-win_default`
- Directory `/home/mello/docker/eplan-win/` (incl. 14G `share/` with EPLAN installers: Electric P8 2024/25/26, Fluid, License Manager, Industry packages, Rehost, ERP-PDM)
- **Reason**: All EPLAN work now runs on the actual Windows PC, VM was redundant.

### 2. Tier-1 safe cleanup — ~275G accounting (Δ on disk)
- `docker builder prune -af` → 61.73G build cache
- `snap remove --revision=<rev>` for 10 disabled snap revisions (code 240, core20 2769, core22 2339, core24 1587, firefox 8339, firmware-updater 224, snap-store 1338, snapd 26382, snapd-desktop-integration 357, spotify 94)
- `journalctl --vacuum-size=500M` → freed 3.5G from `/var/log/journal`
- `rm -rf ~/.cache/uv` (23G)
- `rm -rf ~/.cache/pip` (11G)
- `rm -rf ~/llm-bench/hf` (turned out to be symlinks into `.cache/huggingface/hub`, took 0.13s — real space stayed put)
- `docker image prune -f` + `docker volume prune -f` reported 0B (dangling images referenced by stopped containers; volumes considered in-use)

## Kept (decided this session)

### StemDeck — kept
- Roberto's YouTube → stem-splitter (Demucs `htdemucs_6s`, 6 stems: vocals/drums/bass/guitar/piano/other), FastAPI on :8000, GPU.
- Container exited 13 days ago but stack stays.
- Source at `~/commander/projects/stemdeck` (5.9M).
- Image `stemdeck:mello` (~13G), volume `mello_stemdeck_cache` (Demucs weights).
- Defined as service `stemdeck` in `/home/mello/docker-compose.yml`.

## Remaining big consumers (next cleanup pass)

| Path | Size | Notes |
|---|---|---|
| `~/ComfyUI/models` | 1.3T | diffusion_models 598G, checkpoints 219G, text_encoders 172G, LLM 170G, loras 64G. WAN 2.1 ~63G deprecated by 2.2. BF16/FP8 duplicates ~60G. |
| `~/.ollama/models` | 518G | Old models 4-6 weeks unused: nemotron-3-super:120b (86G), qwen3-coder-next:q8_0 (84G), glm-4.7-flash:bf16 (59G), qwen3.6:35b (23G), nemotron-cascade-2:30b (24G), qwen3.5:35b-a3b (23G), qwen2.5:32b (19G), qwen3.5:27b (17G). |
| `/var/lib/docker` | 233G | Mostly overlay2 + 128G of volumes (claudicle clickhouse 26G, ollama_embed 18G, comfyui_data 9.1G, n8n_postgres 8.6G all in active use). |
| `~/models/huggingface` | 277G | Overlaps with `.cache/huggingface/hub` 224G — same models in both: Qwen3.6-35B-A3B-Claude-4.7-Opus-abliterated, Qwen3.6-27B, talkie-1930-13b-base, Nemotron-Cascade-2-30B-A3B. Needs investigation before deleting either. |
| `~/.cache/huggingface` | 224G | See above. |
| `~/commander` | 76G | Grew 8G during cleanup pass. Worth a drill-down. |

## Synology offload option
`//192.168.2.109/ComfyUI` mounted at `/mnt/synology/ComfyUI` has 1.7T free (only 102G used). Good target for moving older ComfyUI diffusion checkpoints.

## Commands used (for future reference)
```bash
# Survey
df -h
sudo du -h -d 1 -x /home/mello | sort -hr | head -30
sudo docker system df
ollama list

# Docker cleanup
sudo docker builder prune -af
sudo docker image prune -f
sudo docker volume prune -f

# Snap old revisions
snap list --all | awk '/disabled/{print $1, $3}' | while read n r; do sudo snap remove --revision=$r $n; done

# Journal vacuum
sudo journalctl --vacuum-size=500M

# Compose stack full removal
cd <project-dir> && sudo docker compose down -v --rmi all --remove-orphans
```
