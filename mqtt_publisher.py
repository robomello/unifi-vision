"""paho-mqtt wrapper: connect + LWT + retained discovery.

Design note (deviation from the plan's literal wording -- see poller.py):
paho-mqtt supports exactly ONE last-will per client connection, so "register
LWT on each switch availability topic" (N topics) is not something a single
`mqtt.Client` can do. This wrapper exposes one `set_last_will()` used for a
single poller-health topic; poller.py additionally publishes an explicit
`offline` to every per-switch availability topic on graceful shutdown. Hard
crashes (SIGKILL/OOM) are covered by the card's own 20s `ts` staleness gate
(per the design spec), not by per-switch LWT.
"""
from __future__ import annotations

import json
import logging

import paho.mqtt.client as mqtt

logger = logging.getLogger(__name__)

ONLINE = "online"
OFFLINE = "offline"


class MqttPublisher:
    def __init__(self, host: str, port: int, user: str, password: str, client_id: str = "unifi-vision") -> None:
        self.host = host
        self.port = port
        self.client = mqtt.Client(client_id=client_id, callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
        self.client.username_pw_set(user, password)

    def set_last_will(self, topic: str) -> None:
        """Register the poller's single LWT. Must be called before connect()."""
        self.client.will_set(topic, payload=OFFLINE, qos=1, retain=True)

    def connect(self) -> None:
        try:
            self.client.connect(self.host, self.port)
            self.client.loop_start()
        except (OSError, ValueError) as exc:
            raise RuntimeError(f"MQTT connect to {self.host}:{self.port} failed: {exc}") from exc

    def publish_discovery(self, topic: str, config: dict) -> None:
        self._publish(topic, json.dumps(config), retain=True)

    def publish_state(self, topic: str, state: str) -> None:
        self._publish(topic, state, retain=False)

    def publish_attrs(self, topic: str, attrs: dict) -> None:
        self._publish(topic, json.dumps(attrs), retain=False)

    def publish_availability(self, topic: str, online: bool, best_effort: bool = False) -> None:
        self._publish(topic, ONLINE if online else OFFLINE, retain=True, best_effort=best_effort)

    def _publish(self, topic: str, payload: str, retain: bool, best_effort: bool = False) -> None:
        """Publish and confirm delivery. Failures raise RuntimeError so the
        poll loop's backoff engages on a broker outage -- unless best_effort
        (graceful-shutdown path, where raising would mask the shutdown)."""
        try:
            result = self.client.publish(topic, payload, qos=1, retain=retain)
            if result.rc != mqtt.MQTT_ERR_SUCCESS:
                raise RuntimeError(f"publish returned rc={result.rc}")
            result.wait_for_publish(timeout=5)
        except (OSError, ValueError, RuntimeError) as exc:
            logger.error("MQTT publish to %s failed: %s", topic, exc)
            if not best_effort:
                raise RuntimeError(f"MQTT publish to {topic} failed: {exc}") from exc

    def close(self) -> None:
        self.client.loop_stop()
        self.client.disconnect()
