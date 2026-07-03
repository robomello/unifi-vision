"""Main poll loop: fetch -> filter -> deltas -> payloads -> publish.

All exceptions are caught inside the loop with exponential backoff (capped
at MAX_BACKOFF_SEC) -- the container's `restart: unless-stopped` is the only
supervisor, so this process must never crash-loop on a transient UDM Pro or
MQTT hiccup.

LWT note: see mqtt_publisher.py docstring. A single poller-health LWT covers
"the whole poller died"; graceful shutdown (SIGTERM) additionally publishes
an explicit `offline` to every per-switch availability topic.
"""
from __future__ import annotations

import logging
import time

from config import Config
from deltas import DeltaTracker
from filter import select_switches
from mqtt_publisher import MqttPublisher
from payload import (
    attrs_payload,
    attrs_topic,
    availability_topic,
    discovery_config,
    discovery_topic,
    port_attrs,
    slug,
    state_string,
    state_topic,
)
from unifi_client import UniFiClient

logger = logging.getLogger(__name__)

MAX_BACKOFF_SEC = 60
POLLER_HEALTH_TOPIC = "unifi-vision/_poller/availability"


def publish_discovery_for_switches(publisher: MqttPublisher, switches: list[dict], cfg: Config) -> None:
    """Publish retained discovery config for each switch, once at startup."""
    for sw in switches:
        name, mac, model = _switch_identity(sw)
        name_slug = slug(name)
        publisher.publish_discovery(
            discovery_topic(name_slug, cfg.discovery_prefix),
            discovery_config(
                name=name,
                mac=mac,
                model=model,
                discovery_prefix=cfg.discovery_prefix,
                state_prefix=cfg.state_prefix,
            ),
        )


def _switch_identity(sw: dict) -> tuple[str, str, str]:
    name = sw.get("name")
    mac = sw.get("mac")
    if name is None or name == "":
        name = mac if mac is not None else "unknown"
    model = sw.get("model")
    return name, mac if mac is not None else "", model if model is not None else "unknown"


def poll_once(client: UniFiClient, tracker: DeltaTracker, publisher: MqttPublisher, cfg: Config) -> None:
    """One fetch -> filter -> deltas -> publish cycle for every configured switch."""
    devices = client.stat_device()
    switches = select_switches(devices, cfg.switch_macs)

    for sw in switches:
        name, mac, model = _switch_identity(sw)
        name_slug = slug(name)
        raw_ports_field = sw.get("port_table")
        raw_ports = raw_ports_field if raw_ports_field is not None else []

        shaped_ports = []
        up_count = 0
        for raw_port in raw_ports:
            port_idx = raw_port.get("port_idx")
            if port_idx is None:
                # malformed entry; skipping keeps (mac, idx) delta buckets from colliding
                logger.warning("switch %s: port entry without port_idx skipped", name)
                continue
            rx_bytes = raw_port.get("rx_bytes") if raw_port.get("rx_bytes") is not None else 0
            tx_bytes = raw_port.get("tx_bytes") if raw_port.get("tx_bytes") is not None else 0
            rx_bps, tx_bps = tracker.sample(mac, port_idx, rx_bytes, tx_bytes)
            shaped_ports.append(port_attrs(raw_port, rx_bps, tx_bps))
            if raw_port.get("up"):
                up_count += 1

        publisher.publish_state(state_topic(name_slug, cfg.state_prefix), state_string(up_count, len(raw_ports)))
        publisher.publish_attrs(
            attrs_topic(name_slug, cfg.state_prefix),
            attrs_payload(model=model, mac=mac, ports=shaped_ports),
        )
        publisher.publish_availability(availability_topic(name_slug, cfg.state_prefix), online=True)


def publish_shutdown_offline(publisher: MqttPublisher, switches: list[dict], cfg: Config) -> None:
    """Best-effort graceful-shutdown signal: explicit offline per switch + poller health."""
    for sw in switches:
        name, _mac, _model = _switch_identity(sw)
        publisher.publish_availability(
            availability_topic(slug(name), cfg.state_prefix), online=False, best_effort=True
        )
    publisher.publish_availability(POLLER_HEALTH_TOPIC, online=False, best_effort=True)


def _startup(client: UniFiClient, publisher: MqttPublisher, cfg: Config) -> list[dict]:
    """Connect + login + retained discovery, retried with backoff.

    At host boot this container can come up before Mosquitto or the UDM Pro;
    crashing here would defeat the no-crash-loop contract, so keep retrying."""
    publisher.set_last_will(POLLER_HEALTH_TOPIC)
    backoff = cfg.poll_sec
    while True:
        try:
            publisher.connect()
            client.login()
            devices = client.stat_device()
            switches = select_switches(devices, cfg.switch_macs)
            publish_discovery_for_switches(publisher, switches, cfg)
            publisher.publish_availability(POLLER_HEALTH_TOPIC, online=True)
            return switches
        except Exception as exc:  # noqa: BLE001 - retry, never crash-loop at boot
            logger.error("startup failed (retrying in %ss): %s", backoff, exc)
            time.sleep(backoff)
            backoff = min(backoff * 2, MAX_BACKOFF_SEC)


def run(client: UniFiClient, publisher: MqttPublisher, cfg: Config) -> None:
    switches = _startup(client, publisher, cfg)

    tracker = DeltaTracker()
    backoff = cfg.poll_sec

    try:
        while True:
            try:
                poll_once(client, tracker, publisher, cfg)
                backoff = cfg.poll_sec
            except Exception as exc:  # noqa: BLE001 - poller must never crash-loop
                logger.error("poll cycle failed: %s", exc, exc_info=True)
                backoff = min(backoff * 2, MAX_BACKOFF_SEC)
            time.sleep(backoff)
    except KeyboardInterrupt:
        logger.info("shutdown requested, publishing offline state")
        publish_shutdown_offline(publisher, switches, cfg)
        raise
