"""MQTT topic/payload shaping: slug, topics, discovery config, state, attrs. PURE.

This is the shared contract with the unifi-switch-card (built in parallel
against the same shapes). Do not change topic formats or JSON keys here
without updating the plan and the card together.
"""
from __future__ import annotations

import re
import time

DISCOVERY_PREFIX_DEFAULT = "homeassistant"
STATE_PREFIX_DEFAULT = "unifi-vision"
MANUFACTURER = "Ubiquiti"

_SLUG_NON_ALNUM = re.compile(r"[^a-z0-9]+")


def slug(name: str) -> str:
    """Deterministic, ASCII-only slug: lowercase, non-alnum runs -> `_`, edges stripped."""
    if not name:
        return ""
    collapsed = _SLUG_NON_ALNUM.sub("_", name.strip().lower())
    return collapsed.strip("_")


def discovery_topic(name_slug: str, discovery_prefix: str = DISCOVERY_PREFIX_DEFAULT) -> str:
    return f"{discovery_prefix}/sensor/unifi_vision_{name_slug}/config"


def state_topic(name_slug: str, state_prefix: str = STATE_PREFIX_DEFAULT) -> str:
    return f"{state_prefix}/{name_slug}/state"


def attrs_topic(name_slug: str, state_prefix: str = STATE_PREFIX_DEFAULT) -> str:
    return f"{state_prefix}/{name_slug}/attrs"


def availability_topic(name_slug: str, state_prefix: str = STATE_PREFIX_DEFAULT) -> str:
    return f"{state_prefix}/{name_slug}/availability"


def discovery_config(
    name: str,
    mac: str,
    model: str,
    discovery_prefix: str = DISCOVERY_PREFIX_DEFAULT,
    state_prefix: str = STATE_PREFIX_DEFAULT,
) -> dict:
    """Retained HA MQTT-discovery config payload for one switch sensor."""
    name_slug = slug(name)
    return {
        "name": name,
        "unique_id": f"unifi_vision_{name_slug}",
        # Without object_id, HA slugs the entity_id from device+entity name
        # ("Shop Switch" twice -> sensor.shop_switch_shop_switch).
        "object_id": f"unifi_vision_{name_slug}",
        "state_topic": state_topic(name_slug, state_prefix),
        "json_attributes_topic": attrs_topic(name_slug, state_prefix),
        "availability_topic": availability_topic(name_slug, state_prefix),
        "payload_available": "online",
        "payload_not_available": "offline",
        "icon": "mdi:switch",
        "device": {
            "identifiers": [f"unifi_vision_{mac}"],
            "name": name,
            "model": model,
            "manufacturer": MANUFACTURER,
        },
    }


def state_string(up: int, total: int) -> str:
    """e.g. state_string(14, 26) -> "14/26"."""
    return f"{up}/{total}"


def _parse_poe_w(poe_power) -> float:
    """UniFi reports poe_power as a numeric string (e.g. "5.81") or null."""
    if poe_power is None:
        return 0.0
    try:
        return float(poe_power)
    except (TypeError, ValueError):
        return 0.0


def _duplex_label(full_duplex) -> str:
    if full_duplex is None:
        return "?"
    return "full" if full_duplex else "half"


def _parse_rate_bps(value) -> int:
    """UniFi reports live per-port rate as `rx_bytes-r`/`tx_bytes-r` (float
    bytes/sec), already computed by the switch/controller. Use this directly
    instead of our own delta of the cumulative `rx_bytes`/`tx_bytes` counters:
    those counters only update once per the device's controller-inform cycle
    (tens of seconds, see `next_interval`), not every poll, so a naive
    delta-over-5s reads 0 almost every cycle with one artificially inflated
    spike whenever a fresh inform lands -- exactly reproducing the "Main
    Panel Switch shows no transfer rate" bug even while it has real,
    continuous traffic.
    """
    if value is None:
        return 0
    try:
        return max(0, int(value))
    except (TypeError, ValueError):
        return 0


def port_attrs(port: dict) -> dict:
    """Shape one raw port_table entry into the card's port schema.

    Explicit `is None` checks throughout -- speed=0, up=False and rx_bps=0
    are legitimate values, not "missing", so `or`-style falsy defaulting
    would silently corrupt real down-port/idle-port data.
    """
    idx = port.get("port_idx")
    name = port.get("name")
    up = port.get("up")
    speed = port.get("speed")
    media = port.get("media")

    return {
        "idx": idx if idx is not None else port.get("idx"),
        "name": name if name is not None else "?",
        "up": bool(up) if up is not None else False,
        "speed": speed if speed is not None else 0,
        "duplex": _duplex_label(port.get("full_duplex")),
        "poe_w": _parse_poe_w(port.get("poe_power")),
        "rx_bps": _parse_rate_bps(port.get("rx_bytes-r")),
        "tx_bps": _parse_rate_bps(port.get("tx_bytes-r")),
        "media": media if media is not None else "?",
    }


def attrs_payload(model: str, mac: str, ports: list[dict], ts: float | None = None) -> dict:
    """{"model", "mac", "ports": [...], "ts": epoch_seconds}. ts drives the
    card's 20s staleness gate; defaults to now() when not supplied (tests
    should always pass an explicit ts for determinism).
    """
    return {
        "model": model,
        "mac": mac,
        "ports": list(ports),
        "ts": int(ts) if ts is not None else int(time.time()),
    }
