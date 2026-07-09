---
name: SLZB-MR1 Zigbee Coordinator
description: Dual-radio Zigbee coordinator at 192.168.2.99, SMLIGHT SLZB-MR1. "Losing IEEE" is usually TCP listener down on port 7683 after firmware update, not actual IEEE loss.
type: reference
originSessionId: <REDACTED-UUID-34>
---
Device: SLZB-MR1 (SMLIGHT dual-radio coordinator) at `http://192.168.2.99`, firmware v3.2.9.

Radios:
- Radio 0: EFR32MG21, TCP port 6638, firmware 20241105
- Radio 1: CC2652P7, TCP port 7683, firmware 20260307. Custom IEEE `0x00124b0026b8817a`, factory IEEE `0x00124b00294b9a1b`.

"Losing IEEE" decoded: the user-visible complaint almost always means the TCP listener on port 7683 (or 6638) is not bound, not that the chip forgot its address. Firmware updates reset the per-radio exposure mode. Triage first: `nc -zv 192.168.2.99 7683`. If refused while `/ha_info` returns 200 JSON, it's the listener — fix via web UI → Settings → radio 1 mode = LAN/Socket → Tools → Reboot ESP.

Useful endpoints: `/ha_info` (JSON health), `/api2?action=4&cmd=14[&idx=1]` (CUR IEEE), `/api2?action=4&cmd=12[&idx=1]` (FACTORY IEEE), `/api2?action=1&param=crash_info`, `/events` (SSE for async command responses — HTTP body is just `ok`). Full API schema lives in `/js/httpApi.js` on the device itself.

Full diagnostic cheatsheet in Obsidian: `50-Reference/slzb-mr1-zigbee-coordinator.md`.

Monitor decision (2026-04-23): Roberto opted to wait — don't build monitoring until it fails again. When it does, the shape is: Python script mirroring `vram_guard.py`, systemd user timer every 2 min, three checks (`/ha_info` 200, TCP 6638 open, TCP 7683 open), Telegram-on-transition via `TELEGRAM_JOE_TOKEN` to `TELEGRAM_NOTIFICATION_CHAT_ID`, detect-only (no auto-remediation). Do not rebuild from scratch — lift the `vram_guard.py` Telegram block and `matomo-report.service` timer pattern.
