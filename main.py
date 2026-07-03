"""Entrypoint: wire config -> UniFi client -> MQTT publisher -> poll loop."""
from __future__ import annotations

import logging
import signal
import sys

from config import load_config
from mqtt_publisher import MqttPublisher
from poller import run
from unifi_client import UniFiClient

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def _sigterm(_signum, _frame) -> None:
    # docker stop sends SIGTERM; route it through the same graceful-shutdown
    # path as SIGINT so the per-switch offline publishes actually happen
    raise KeyboardInterrupt


def main() -> int:
    signal.signal(signal.SIGTERM, _sigterm)
    try:
        cfg = load_config()
    except RuntimeError as exc:
        logger.error("config error: %s", exc)
        return 1

    client = UniFiClient(cfg.unifi_host, cfg.unifi_user, cfg.unifi_pass, cfg.unifi_site)
    publisher = MqttPublisher(cfg.mqtt_host, cfg.mqtt_port, cfg.mqtt_user, cfg.mqtt_pass)

    try:
        run(client, publisher, cfg)
    except KeyboardInterrupt:
        logger.info("stopped by signal")
    finally:
        client.close()
        publisher.close()

    return 0


if __name__ == "__main__":
    sys.exit(main())
