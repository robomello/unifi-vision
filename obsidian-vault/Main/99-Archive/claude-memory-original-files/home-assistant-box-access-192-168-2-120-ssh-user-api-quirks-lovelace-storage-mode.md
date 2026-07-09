---
name: Home Assistant box access (192.168.2.120) — SSH user, API quirks, Lovelace storage mode
description: How to reach and manage the HAOS instance: SSH is user hassio not root, Supervisor API needs the websocket proxy not REST, Lovelace is storage-mode, HACS is actually installed
type: reference
---

Home Assistant instance details discovered while building unifi-vision (2026-07-03):
- HA runs on separate hardware at 192.168.2.120:8123 (HAOS Supervisor). Long-lived admin token already exists in ~/.config/zigbee-watchdog/watchdog.env (HA_URL/HA_TOKEN).
- HACS IS installed (contradicts an earlier assumption of 'no HACS') — confirmed via lovelace_resources storage showing /hacsfiles/* entries (apexcharts-card, mushroom, bubble-card, button-card, etc.).
- SSH add-on (a0d7b954_ssh) runs as user 'hassio' (uid 1000, in wheel group with passwordless sudo), NOT root — SSH as root will always fail on this box.
- The HA Supervisor REST API at /api/hassio/* returns 401 with the long-lived token even though the token is valid admin (confirmed via /api/config = 200). Use the WEBSOCKET API instead: connect to ws://192.168.2.120:8123/api/websocket, auth, then send {type: 'supervisor/api', endpoint: '/addons/...', method: 'get'|'post'} — this proxies through fine and can manage add-on options (e.g. appending SSH authorized_keys) and restart add-ons.
- Lovelace is in storage mode (not YAML) with 3 dashboards: dashboard-roberto, dashboard-gisele, map. Resources and dashboard views can be added via websocket commands lovelace/resources/create and lovelace/config + lovelace/config/save (get current config, append to views[], save back — there's no 'add single view' shortcut).
- Entity registry renames: lovelace/config/entity_registry/... no — use config/entity_registry/list and config/entity_registry/update with new_entity_id to fix bad auto-generated entity_ids.
