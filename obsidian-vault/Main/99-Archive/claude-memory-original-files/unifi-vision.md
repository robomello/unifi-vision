---
name: UniFi Vision
description: UniFi camera integration at /home/mello/commander/projects/unifi-vision/. Polls UniFi Protect, publishes to MQTT for Home Assistant. Container: unifi-vision (internal-only).
type: project
---

## UniFi Vision Project (2026-07-03)

**Location:** /home/mello/commander/projects/unifi-vision/
**Container:** unifi-vision (running, internal-only, no tunnel)
**Status:** Active as of Jul 3

### What It Does
UniFi camera integration for Home Assistant. Polls UniFi Protect API, publishes camera events to MQTT for HA consumption.

### Architecture
- Python FastAPI app
- MQTT publisher for HA integration
- Polls UniFi Protect API for camera events
- Docker container (no public exposure)

### Key Files
- main.py (FastAPI app)
- poller.py (UniFi API polling)
- mqtt_publisher.py (MQTT integration)
- payload.py (event formatting)
- filter.py (event filtering)
- config.py (configuration)
- card/ (HA dashboard card)
- deploy/ (deployment configs)

### Gotchas (from memory entry)
- browser-agent drifted to Playwright during this project despite Lightpanda-only preference
- Agent definition file still hardcodes Playwright with networkidle
- Playwright hangs on networkidle against apps with persistent WebSocket (like Home Assistant)
- Fix: waitUntil:'domcontentloaded' + explicit DOM selector waits

Why: Recent project (Jul 3) not yet in project memory. Involves UniFi Protect + Home Assistant + MQTT integration.

How to apply: When working on UniFi camera features or HA MQTT integrations, this is the project. Container is internal-only (no CF tunnel).
