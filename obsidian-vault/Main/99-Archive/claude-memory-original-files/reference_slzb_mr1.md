---
name: SLZB-MR1 Zigbee Coordinator
description: Dual-radio Zigbee coordinator at 192.168.2.99, SMLIGHT SLZB-MR1. "Losing IEEE" is usually TCP listener down on port 7683 after firmware update, not actual IEEE loss.
type: reference
originSessionId: <REDACTED-UUID-34>
---
SLZB-MR1 dual-radio Zigbee coordinator at `http://192.168.2.99` (SMLIGHT, firmware v3.2.9). Radio 0 = EFR32MG21 on TCP 6638; Radio 1 = CC2652P7 on TCP 7683.

**Quick triage — "Losing IEEE":** almost always the TCP listener on 7683 (or 6638) is unbound after a firmware update, NOT the chip losing its address. Check `nc -zv 192.168.2.99 7683`; if refused while `/ha_info` returns 200, fix via web UI → Settings → radio 1 mode = LAN/Socket → Reboot ESP.

**Full reference (source of truth):** `50-Reference/slzb-mr1-zigbee-coordinator.md` — complete IEEE addresses (custom/factory, both radios), ESP32 host MAC, pending firmware, full diagnostic script, the `/api2` action/cmd table, and the failed-flash NVS-corruption recovery all live there. Don't duplicate them here.

Monitor decision (2026-04-23): Roberto opted to wait — don't build monitoring until it fails again. When it does, the shape is: Python script mirroring `vram_guard.py`, systemd user timer every 2 min, three checks (`/ha_info` 200, TCP 6638 open, TCP 7683 open), Telegram-on-transition via `TELEGRAM_JOE_TOKEN` to `TELEGRAM_NOTIFICATION_CHAT_ID`, detect-only (no auto-remediation). Do not rebuild from scratch — lift the `vram_guard.py` Telegram block and `matomo-report.service` timer pattern.
