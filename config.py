"""Env-driven configuration. Immutable: `Config` is a frozen dataclass built
once at startup by `load_config()`. Secrets only via env -- never hardcoded.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

ENV_PATH = Path.home() / ".env"

# Speed (bps) -> LED color tier. The card owns rendering; these constants are
# documented here (and duplicated as JS constants in the card) as the single
# source of truth for the tier boundaries.
SPEED_COLOR_TIERS: dict[str, tuple[int, ...]] = {
    "amber": (10, 100),
    "green": (1000,),
    "blue": (2500, 5000, 10000),
}

# Traffic (bytes/s) -> flash-rate tier boundaries.
TRAFFIC_TIER_IDLE_MAX_BPS = 1_000          # < 1 KB/s -> idle / solid
TRAFFIC_TIER_LOW_MAX_BPS = 1_000_000       # < 1 MB/s -> low / slow-flash
# >= TRAFFIC_TIER_LOW_MAX_BPS -> high / fast-flash


def load_env_file(path: Path = ENV_PATH) -> dict[str, str]:
    """Parse a `.env`-style file, skipping malformed lines. Never raises if missing."""
    env: dict[str, str] = {}
    if not path.exists():
        return env
    for line in path.read_text().splitlines():
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        if key.isidentifier():
            env[key] = value.strip().strip('"').strip("'")
    return env


def _get(env: dict[str, str], key: str, default: str | None = None) -> str | None:
    """Prefer process env (compose `environment:`), fall back to parsed .env file.

    Empty strings count as unset: compose maps `KEY: ${VAR}` to `KEY=` when
    VAR is blank, which must not shadow a documented default.
    """
    value = os.environ.get(key)
    if value is not None and value != "":
        return value
    value = env.get(key)
    if value is not None and value != "":
        return value
    return default


def _get_int(env: dict[str, str], key: str, default: str) -> int:
    """Like _get but parsed as int; raises RuntimeError (the documented
    fail-fast contract) instead of a bare ValueError on malformed values."""
    raw = _get(env, key, default)
    try:
        return int(raw)
    except (TypeError, ValueError) as exc:
        raise RuntimeError(f"unifi-vision config: {key} must be an integer, got {raw!r}") from exc


@dataclass(frozen=True)
class Config:
    unifi_host: str
    unifi_user: str
    unifi_pass: str
    unifi_site: str
    mqtt_host: str
    mqtt_port: int
    mqtt_user: str
    mqtt_pass: str
    switch_macs: str
    poll_sec: int
    discovery_prefix: str
    state_prefix: str


def load_config(env_file_path: Path = ENV_PATH) -> Config:
    """Build immutable Config from process env + `.env` fallback.

    Raises RuntimeError with a descriptive message if a required credential
    is missing -- fail fast at startup rather than mid-poll.
    """
    file_env = load_env_file(env_file_path)

    unifi_user = _get(file_env, "UNIFI_USER")
    unifi_pass = _get(file_env, "UNIFI_PASS")
    mqtt_host = _get(file_env, "MQTT_HOST")
    mqtt_user = _get(file_env, "MQTT_USER")
    mqtt_pass = _get(file_env, "MQTT_PASS")

    missing = [
        name
        for name, value in (
            ("UNIFI_USER", unifi_user),
            ("UNIFI_PASS", unifi_pass),
            ("MQTT_HOST", mqtt_host),
            ("MQTT_USER", mqtt_user),
            ("MQTT_PASS", mqtt_pass),
        )
        if not value
    ]
    if missing:
        raise RuntimeError(f"unifi-vision config missing required env vars: {', '.join(missing)}")

    return Config(
        unifi_host=_get(file_env, "UNIFI_HOST", "https://192.168.1.1"),
        unifi_user=unifi_user,
        unifi_pass=unifi_pass,
        unifi_site=_get(file_env, "UNIFI_SITE", "default"),
        mqtt_host=mqtt_host,
        mqtt_port=_get_int(file_env, "MQTT_PORT", "1883"),
        mqtt_user=mqtt_user,
        mqtt_pass=mqtt_pass,
        switch_macs=_get(file_env, "SWITCH_MACS", ""),
        poll_sec=_get_int(file_env, "POLL_SEC", "5"),
        discovery_prefix=_get(file_env, "DISCOVERY_PREFIX", "homeassistant"),
        state_prefix=_get(file_env, "STATE_PREFIX", "unifi-vision"),
    )
