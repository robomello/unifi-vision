"""Unit tests for payload.py — slugs, topics, discovery config, state, attrs (PURE).

The exact topic strings and JSON shapes here are the MQTT contract shared
with the unifi-switch-card (built in parallel against this same contract).
Do not change these shapes without updating the plan.
"""
from __future__ import annotations

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


class TestSlug:
    def test_simple_name(self):
        assert slug("Shop Switch") == "shop_switch"

    def test_punctuation_collapses_to_single_underscore(self):
        assert slug("US-24-250W!!") == "us_24_250w"

    def test_multiple_spaces_collapse(self):
        assert slug("Multi   Space   Name") == "multi_space_name"

    def test_leading_trailing_stripped(self):
        assert slug("  Shop Switch  ") == "shop_switch"

    def test_leading_trailing_punctuation_stripped(self):
        assert slug("--Shop Switch--") == "shop_switch"

    def test_unicode_non_ascii_replaced(self):
        assert slug("Büro Switch") == "b_ro_switch"

    def test_already_slug_stable(self):
        assert slug("shop_switch") == "shop_switch"

    def test_empty_string(self):
        assert slug("") == ""

    def test_mixed_case(self):
        assert slug("SHOP Switch") == "shop_switch"

    def test_deterministic(self):
        assert slug("Main Panel Switch") == slug("Main Panel Switch")


class TestTopics:
    def test_discovery_topic_default_prefix(self):
        assert (
            discovery_topic("shop_switch")
            == "homeassistant/sensor/unifi_vision_shop_switch/config"
        )

    def test_discovery_topic_custom_prefix(self):
        assert (
            discovery_topic("shop_switch", discovery_prefix="ha-custom")
            == "ha-custom/sensor/unifi_vision_shop_switch/config"
        )

    def test_state_topic(self):
        assert state_topic("shop_switch") == "unifi-vision/shop_switch/state"

    def test_attrs_topic(self):
        assert attrs_topic("shop_switch") == "unifi-vision/shop_switch/attrs"

    def test_availability_topic(self):
        assert availability_topic("shop_switch") == "unifi-vision/shop_switch/availability"

    def test_state_topic_custom_prefix(self):
        assert state_topic("shop_switch", state_prefix="uv") == "uv/shop_switch/state"


class TestDiscoveryConfig:
    def test_has_required_ha_keys(self):
        cfg = discovery_config(name="Shop Switch", mac="aa:bb:cc:11:22:33", model="US24P250")
        assert cfg["name"] == "Shop Switch"
        assert cfg["unique_id"] == "unifi_vision_shop_switch"
        assert cfg["object_id"] == "unifi_vision_shop_switch"
        assert cfg["state_topic"] == "unifi-vision/shop_switch/state"
        assert cfg["json_attributes_topic"] == "unifi-vision/shop_switch/attrs"
        assert cfg["availability_topic"] == "unifi-vision/shop_switch/availability"
        assert cfg["payload_available"] == "online"
        assert cfg["payload_not_available"] == "offline"
        assert cfg["icon"] == "mdi:switch"

    def test_has_device_block(self):
        cfg = discovery_config(name="Shop Switch", mac="aa:bb:cc:11:22:33", model="US24P250")
        device = cfg["device"]
        assert device["identifiers"] == ["unifi_vision_aa:bb:cc:11:22:33"]
        assert device["name"] == "Shop Switch"
        assert device["model"] == "US24P250"
        assert device["manufacturer"] == "Ubiquiti"

    def test_unique_id_matches_slug_of_name(self):
        cfg = discovery_config(name="Main Panel Switch", mac="11:22:33:44:55:66", model="US8P150")
        assert cfg["unique_id"] == "unifi_vision_main_panel_switch"


class TestStateString:
    def test_normal(self):
        assert state_string(14, 26) == "14/26"

    def test_all_up(self):
        assert state_string(8, 8) == "8/8"

    def test_all_down(self):
        assert state_string(0, 8) == "0/8"

    def test_zero_total(self):
        assert state_string(0, 0) == "0/0"


class TestPortAttrs:
    def test_normal_port(self):
        port = {
            "port_idx": 1,
            "name": "Port 1",
            "up": True,
            "speed": 1000,
            "full_duplex": True,
            "poe_power": "5.81",
            "media": "GE",
            "rx_bytes-r": 12000.7,
            "tx_bytes-r": 4000.2,
        }
        result = port_attrs(port)
        assert result == {
            "idx": 1,
            "name": "Port 1",
            "up": True,
            "speed": 1000,
            "duplex": "full",
            "poe_w": 5.81,
            "rx_bps": 12000,
            "tx_bps": 4000,
            "media": "GE",
        }

    def test_half_duplex(self):
        port = {"port_idx": 1, "name": "Port 1", "up": True, "speed": 100, "full_duplex": False, "media": "GE"}
        result = port_attrs(port)
        assert result["duplex"] == "half"

    def test_missing_full_duplex_defaults_to_unknown(self):
        port = {"port_idx": 1, "name": "Port 1", "up": False, "speed": 0, "media": "GE"}
        result = port_attrs(port)
        assert result["duplex"] == "?"

    def test_missing_poe_power_defaults_zero(self):
        port = {"port_idx": 25, "name": "SFP 1", "up": False, "speed": 0, "media": "SFP"}
        result = port_attrs(port)
        assert result["poe_w"] == 0.0

    def test_none_poe_power_defaults_zero(self):
        port = {"port_idx": 25, "name": "SFP 1", "up": False, "speed": 0, "poe_power": None, "media": "SFP"}
        result = port_attrs(port)
        assert result["poe_w"] == 0.0

    def test_string_poe_power_parsed_to_float(self):
        port = {"port_idx": 6, "name": "Port 6", "up": True, "speed": 100, "poe_power": "1.20", "media": "GE"}
        result = port_attrs(port)
        assert result["poe_w"] == 1.2

    def test_unparseable_poe_power_defaults_zero(self):
        port = {"port_idx": 6, "name": "Port 6", "up": True, "speed": 100, "poe_power": "n/a", "media": "GE"}
        result = port_attrs(port)
        assert result["poe_w"] == 0.0

    def test_missing_media_defaults_to_unknown(self):
        port = {"port_idx": 1, "name": "Port 1", "up": True, "speed": 1000}
        result = port_attrs(port)
        assert result["media"] == "?"

    def test_zero_rx_tx_bps_preserved_not_defaulted(self):
        """0 is a legitimate value and must not be treated as falsy-missing."""
        port = {"port_idx": 1, "name": "Port 1", "up": False, "speed": 0, "media": "GE"}
        result = port_attrs(port)
        assert result["rx_bps"] == 0
        assert result["tx_bps"] == 0
        assert result["speed"] == 0
        assert result["up"] is False

    def test_missing_rate_fields_default_zero(self):
        """Older firmware or a device mid-inform might omit rx_bytes-r/tx_bytes-r."""
        port = {"port_idx": 1, "name": "Port 1", "up": True, "speed": 1000, "media": "GE"}
        result = port_attrs(port)
        assert result["rx_bps"] == 0
        assert result["tx_bps"] == 0

    def test_rate_fields_truncated_to_int(self):
        port = {"port_idx": 1, "name": "Port 1", "up": True, "speed": 1000, "media": "GE",
                "rx_bytes-r": 638996.7744809765, "tx_bytes-r": 26245.21072796935}
        result = port_attrs(port)
        assert result["rx_bps"] == 638996
        assert result["tx_bps"] == 26245

    def test_negative_rate_field_clamped_to_zero(self):
        port = {"port_idx": 1, "name": "Port 1", "up": True, "speed": 1000, "media": "GE",
                "rx_bytes-r": -5.0, "tx_bytes-r": 0}
        result = port_attrs(port)
        assert result["rx_bps"] == 0
        assert result["tx_bps"] == 0

    def test_unparseable_rate_field_defaults_zero(self):
        port = {"port_idx": 1, "name": "Port 1", "up": True, "speed": 1000, "media": "GE",
                "rx_bytes-r": "n/a", "tx_bytes-r": None}
        result = port_attrs(port)
        assert result["rx_bps"] == 0
        assert result["tx_bps"] == 0


class TestAttrsPayload:
    def test_shape(self):
        ports = [
            {
                "idx": 1,
                "name": "Port 1",
                "up": True,
                "speed": 1000,
                "duplex": "full",
                "poe_w": 3.2,
                "rx_bps": 12000,
                "tx_bps": 4000,
                "media": "GE",
            }
        ]
        result = attrs_payload(model="US24P250", mac="aa:bb:cc:11:22:33", ports=ports, ts=1720000000)
        assert result["model"] == "US24P250"
        assert result["mac"] == "aa:bb:cc:11:22:33"
        assert result["ports"] == ports
        assert result["ts"] == 1720000000

    def test_ts_defaults_to_now_when_not_supplied(self):
        result = attrs_payload(model="US24P250", mac="aa:bb:cc:11:22:33", ports=[])
        assert isinstance(result["ts"], int)
        assert result["ts"] > 0

    def test_empty_ports_list(self):
        result = attrs_payload(model="US24P250", mac="aa:bb:cc:11:22:33", ports=[], ts=1720000000)
        assert result["ports"] == []

    def test_does_not_mutate_input_ports_list(self):
        ports = [{"idx": 1, "name": "Port 1"}]
        original_id = id(ports)
        attrs_payload(model="US24P250", mac="aa:bb:cc:11:22:33", ports=ports, ts=1720000000)
        assert id(ports) == original_id
        assert ports == [{"idx": 1, "name": "Port 1"}]
