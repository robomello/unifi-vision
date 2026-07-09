---
name: Home Hardware & Smart Home
description: Home network, smart home, 3D printers, and home-server services running alongside the main rig
type: reference
---

# Home Hardware & Smart Home Inventory

Server hardware (CPU, RAM, GPUs, storage) is documented in `~/.claude/rules/context.md` and `~/CLAUDE.md` -- not duplicated here. This memory covers everything **around** the server: network gear, smart home, 3D printers, and the home-side services running on the rig.

## Network

- **Synology NAS** -- `192.168.2.109`, DSM at `https://192.168.2.109:5001` (see [[synology-nas]])
- **SLZB-MR1 Zigbee Coordinator** -- `192.168.2.99`, dual-radio (see [[reference_slzb_mr1]])
- **UniFi** -- [TBD: controller IP, gateway model, switches, APs, VLAN layout]
- **LAN subnet** -- 192.168.2.0/24 (inferred from existing devices)
- **WAN / ISP** -- [TBD]

## Smart Home

- **Home Assistant** -- [TBD: install type (HA OS / Container / Supervised), host, IP, port, integrations]
- **ESPHome** -- configs at `/home/mello/esphome-configs/` (`commander.yaml`, `secrets.yaml` present)
- **Zigbee** -- via SLZB-MR1 (above); coordinator software [TBD: ZHA / Zigbee2MQTT / etc.]
- **Nest thermostat** -- managed via `nest-agent` (SDM API)

## 3D Printers (Bambu)

- **Models** -- [TBD: e.g., X1C, P1S, A1, A1 mini]
- **Network** -- [TBD: LAN IPs or LAN-only / cloud mode]
- **Slicer** -- [TBD: Bambu Studio / OrcaSlicer]
- **Filament storage** -- [TBD]

## Home-Server Services (cmd.synai.ai rig)

- **Commander** -- main project at `/home/mello/commander/`; UI at `cmd.synai.ai` (port 8070); GPU 1 bound
- **n8n** -- `n8n.synai.ai` (5678), GPU 1
- **ComfyUI** -- `comfyui.synai.ai` (8188), GPU 0 (primary, 600W)
- **NocoDB** -- `nocodb.synai.ai` (8090)
- **Whisper STT** -- internal only, port 8058, GPU 0
- **Street Camera Bot** -- internal only, port 8098, GPU 1
- See full port list in `~/.claude/rules/context.md`

## What to fill in next

When Roberto has 5 minutes, fill the [TBD] blocks. Save updates with:

```bash
echo "..." | python3 ~/skills/obsidian/save-memory.py \
  --section "Infrastructure" --title "Home Hardware & Smart Home" \
  --type reference --description "..."
```
(save-memory replaces an existing same-titled entry's manifest line.)
