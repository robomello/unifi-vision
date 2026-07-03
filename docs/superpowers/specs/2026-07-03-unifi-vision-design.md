# unifi-vision — Live UniFi Switch Faceplate Cards for Home Assistant

**Date:** 2026-07-03
**Status:** Draft — awaiting Roberto's review
**Inspiration:** The unreleased "cisco-vision" card from the HA Facebook group (photorealistic Cisco faceplate, per-port LEDs on live SNMP data). That project is private; we build our own for UniFi.

## Goal

Home Assistant dashboard cards that render each UniFi switch as a near-photorealistic faceplate with live per-port LEDs:

- LED color = negotiated link speed (amber = 10/100M, green = 1G, blue = 2.5G/10G/SFP+, dark = down)
- LED flash rate = live traffic (3 tiers by bytes/s between polls, ~5s poll)
- PoE badge with live wattage on powered ports
- Hover/tap = port detail popup (port name, speed, duplex, PoE W, RX/TX rates)
- Target density: 2–3 switches visible per screen

## Hardware in scope (verified live from UDM Pro API, 2026-07-03)

| Switch | Model | Ports | Notes |
|---|---|---|---|
| Shop Switch | US24P250 | 24 + 2 SFP | flagship card |
| Main Panel Switch | US8P150 | 8 + 2 SFP | |
| US 8 60W | US8P60 | 8 | |
| Theater Switch | US8P60 | 8 | |
| Bridge Garage UP Switch | USF5P (Flex 5) | 5 | |
| Helium Switches | USL16LP (Lite 16 PoE) | 16 | |
| Mello Home | UDMPRO | 8 + 2 SFP+ + WAN | optional card |

Switch list is config-driven; adding a future switch = add its MAC + model to config (new models need a port-geometry map, see below).

## Verified facts this design rests on

- UDM Pro `stat/device` API returns per-port: `up`, `speed`, `full_duplex`, `poe_power`, `poe_enable`, `rx_bytes`, `tx_bytes`, `media`, `name` (verified with live query via existing `~/commander/tools/unifi_network.py` auth).
- HA box (HAOS at `192.168.2.120:8123`) runs a Mosquitto broker — port 1883 open (Zigbee2MQTT rides it).
- Existing HA long-lived token works for core REST API (200 on `/api/config`); Supervisor endpoints return 401 (not needed).
- SSH (22) and Samba (445) are open on the HA box → card JS deployable to `/config/www/`.
- No HACS installed; card will be installed as a manual Lovelace resource (HACS not required).

## Approaches considered

**A. Own poller → MQTT discovery → custom card (CHOSEN).** A small container on the home server polls the UDM Pro every 5s, publishes one MQTT-discovery entity per switch (port array as attributes). Custom Lovelace card renders the faceplate from those attributes. Pros: 5s freshness, exact data shape we want (up/down + deltas, which the official integration lacks), 7 entities instead of ~200. Cons: one more container + MQTT credential setup.

**B. Official HA UniFi integration + custom card.** No new service, but: per-port sensors are disabled-by-default and explode into ~3 entities × ~80 ports, there is no port up/down sensor (only speed/bandwidth), update cadence is slower, and card config would need dozens of entity IDs per switch. Rejected.

**C. Existing HACS `switch_port_card` + official integration.** Least effort, but it's a colored-dot grid — not the faceplate look that motivated this project, and still inherits B's data gaps. Rejected.

## Architecture (Approach A)

```
UDM Pro (192.168.2.1)
   │ HTTPS /proxy/network/api/s/default/stat/device, poll 5s
   ▼
unifi-vision poller (Docker, home server)
   │ MQTT publish (discovery + state, retained config)
   ▼
Mosquitto (HA box :1883)
   ▼
HA MQTT discovery → sensor.unifi_vision_<switch> (state: "14/26", attrs: ports[])
   ▼
unifi-switch-card.js (Lovelace, /config/www/) → SVG faceplate render
```

### Component 1: poller (`commander/projects/unifi-vision/`)

- Python 3.12, `httpx` + `paho-mqtt`. Auth pattern copied from `unifi_network.py` (cookie + X-CSRF-Token, re-login on 401).
- Every 5s: fetch `stat/device`, filter to configured switch MACs, compute per-port `rx_bps`/`tx_bps` from byte-counter deltas (handle counter reset → clamp to 0).
- Publish per switch:
  - Discovery config (retained) → `homeassistant/sensor/unifi_vision_<slug>/config`, device block per switch (model, MAC, name).
  - State → `unifi-vision/<slug>/state` (payload: `"<up>/<total>"`), attributes JSON → `unifi-vision/<slug>/attrs`: `{model, mac, ports: [{idx, name, up, speed, duplex, poe_w, rx_bps, tx_bps, media}], ts}`.
  - Availability topic with LWT → card can grey out on poller death.
- Publish only on change OR every 5s regardless (payloads are ~2–4 KB; always-publish keeps `ts` fresh for staleness detection — chosen).
- Config via env: `UNIFI_HOST/USER/PASS` (reuse existing `.env` values), `MQTT_HOST/USER/PASS`, `SWITCH_MACS` (empty = all `usw` + `udm` devices), `POLL_SEC=5`.
- Errors: try/except around poll loop with exponential backoff (5s→60s cap); descriptive logs; no crash-loop.

### Component 2: card (`unifi-switch-card.js`)

- Single-file vanilla JS custom element (Lit-free, no build step), <800 lines. Deployed to HA `/config/www/unifi-vision/` + registered as Lovelace resource.
- Config: `type: custom:unifi-switch-card`, `entity: sensor.unifi_vision_shop_switch`. Model read from attributes; optional overrides (`title`, `show_poe`, `led_mode`).
- Rendering: inline SVG per model — brushed-metal faceplate (gradients/filters, near-photo look), exact port grid geometry from a `PORT_GEOMETRY` map keyed by model (`US24P250`, `US8P150`, `US8P60`, `USF5P`, `USL16LP`, `UDMPRO`). Unknown model → generic N-port layout, never a blank card.
- LEDs: color by speed (above), CSS keyframe flash at 3 rates by traffic tier (idle <1KB/s solid, low <1MB/s slow flash, high fast flash). PoE ⚡ + wattage under powered ports. SFP ports drawn as SFP cages.
- Interactions: hover tooltip (desktop) / tap popup (mobile) with port detail. Staleness: `ts` older than 20s → desaturate card + "STALE" ribbon.
- Theme-aware: respects HA dark/light themes.

### Component 3: dashboard

- New HA dashboard view "Network" with one card per switch, vertical stack, Shop Switch on top. Added via HA UI or YAML — final wiring verified in a real browser (browser-agent screenshot).

## Phase 0 — Prerequisites (before any implementation)

| Item | How | Status |
|---|---|---|
| MQTT credentials on HA Mosquitto | Create `unifi-vision` user via Mosquitto add-on config (SSH to HA box) or reuse existing broker login | ❗needs Roberto or SSH creds |
| SSH/Samba login to HA box | Needed to deploy card JS + Mosquitto config | ❗confirm credentials |
| `paho-mqtt`, `httpx` | In poller image (`python:3.12-slim` + pip) | pull at build |
| UDM Pro creds | Already in `~/.env` (`UNIFI_USER/PASS`) — reused | ✅ verified working |
| Verify MQTT discovery enabled in HA | Check `mqtt:` integration config once creds exist | pending |

## Testing

- **Unit (pytest):** delta computation (incl. counter reset), payload shaping, switch filtering, discovery topic format. 80%+ on poller logic.
- **Integration:** poller against live UDM Pro + a throwaway MQTT topic; assert entity appears in HA via REST API (`/api/states/sensor.unifi_vision_shop_switch`).
- **E2E/UI (mandatory per agent-behavior Rule 5):** browser-agent loads the HA dashboard, screenshots each switch card, confirms LEDs/colors/PoE badges render; plug/unplug validation on one port (speed change reflected within ~10s).

## Security

- No new secrets in code; all via env / `.env`. MQTT user scoped with ACL to `unifi-vision/#` + `homeassistant/sensor/unifi_vision_*` if Mosquitto ACLs are in use.
- Poller is read-only against UniFi (GET only). No port control in v1.
- No new exposed ports; poller has no listening socket. Internal-only (no Cloudflare route needed).

## Out of scope (v1)

- Port control (enable/disable, PoE cycle) from the card — v2 candidate, needs write auth + confirm-dialog UX.
- VLAN/port-profile display — v2 (data available in `port_table`, add to tooltip later).
- UniFi Express (UX) + in-wall AP pass-through ports — cards only for real switches + UDM Pro.

## Open questions for Roberto

1. Visual style assumed **photorealistic-leaning SVG** (no answer to the style question — re-confirm). ComfyUI-generated raster faceplates were considered and rejected: port positions must be pixel-exact for LED overlay; SVG gives that deterministically.
2. Include the UDM Pro card in v1? (assumed yes)
3. MQTT credentials — provide, or approve me SSHing into the HA box to create the user?
