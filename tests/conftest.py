"""Shared pytest fixtures for unifi-vision tests.

The device fixtures below are a redacted/trimmed capture of one live UDM Pro
`stat/device` response (2026-07-03). MACs are replaced with placeholder
values; only the keys the poller actually reads are kept.
"""
from __future__ import annotations

import copy

import pytest

SHOP_SWITCH_MAC = "aa:bb:cc:11:22:33"
US8P60_MAC = "aa:bb:cc:11:22:44"
UDMPRO_MAC = "aa:bb:cc:11:22:55"
AP_MAC = "aa:bb:cc:11:22:66"


def _shop_switch() -> dict:
    """usw / US24P250: PoE ports at two speeds + two unused SFP cages."""
    return {
        "type": "usw",
        "name": "Shop Switch",
        "model": "US24P250",
        "mac": SHOP_SWITCH_MAC,
        "port_table": [
            {
                "port_idx": 1,
                "name": "Port 1",
                "up": True,
                "speed": 1000,
                "full_duplex": True,
                "poe_power": "0.00",
                "poe_enable": False,
                "rx_bytes": 10076050514927,
                "tx_bytes": 578551961029,
                "media": "GE",
            },
            {
                "port_idx": 2,
                "name": "Port 2",
                "up": True,
                "speed": 1000,
                "full_duplex": True,
                "poe_power": "5.81",
                "poe_enable": True,
                "rx_bytes": 161690,
                "tx_bytes": 32524100072,
                "media": "GE",
            },
            {
                "port_idx": 6,
                "name": "Port 6",
                "up": True,
                "speed": 100,
                "full_duplex": True,
                "poe_power": "1.20",
                "poe_enable": True,
                "rx_bytes": 190353457962,
                "tx_bytes": 5751229521049,
                "media": "GE",
            },
            {
                "port_idx": 25,
                "name": "SFP 1",
                "up": False,
                "speed": 0,
                "full_duplex": False,
                "poe_power": None,
                "poe_enable": None,
                "rx_bytes": 0,
                "tx_bytes": 0,
                "media": "SFP",
            },
            {
                "port_idx": 26,
                "name": "SFP 2",
                "up": False,
                "speed": 0,
                "full_duplex": False,
                "poe_power": None,
                "poe_enable": None,
                "rx_bytes": 0,
                "tx_bytes": 0,
                "media": "SFP",
            },
        ],
    }


def _us8p60() -> dict:
    """usw / US8P60: two down ports, no PoE data reported (null fields)."""
    return {
        "type": "usw",
        "name": "US 8 60W",
        "model": "US8P60",
        "mac": US8P60_MAC,
        "port_table": [
            {
                "port_idx": 1,
                "name": "Port 1",
                "up": False,
                "speed": 0,
                "full_duplex": False,
                "poe_power": None,
                "poe_enable": None,
                "rx_bytes": 0,
                "tx_bytes": 0,
                "media": "GE",
            },
            {
                "port_idx": 3,
                "name": "Port 3",
                "up": False,
                "speed": 0,
                "full_duplex": False,
                "poe_power": None,
                "poe_enable": None,
                "rx_bytes": 0,
                "tx_bytes": 0,
                "media": "GE",
            },
        ],
    }


def _mello_home_udm() -> dict:
    """udm / UDMPRO: GE port + SFP+ uplink."""
    return {
        "type": "udm",
        "name": "Mello Home",
        "model": "UDMPRO",
        "mac": UDMPRO_MAC,
        "port_table": [
            {
                "port_idx": 1,
                "name": "Port 1",
                "up": True,
                "speed": 1000,
                "full_duplex": True,
                "poe_power": "0.00",
                "poe_enable": False,
                "rx_bytes": 13988774434,
                "tx_bytes": 332100569283,
                "media": "GE",
            },
            {
                "port_idx": 10,
                "name": "SFP+ 1",
                "up": True,
                "speed": 1000,
                "full_duplex": True,
                "poe_power": "0.00",
                "poe_enable": False,
                "rx_bytes": 102451586610,
                "tx_bytes": 11213754103,
                "media": "SFP+",
            },
        ],
    }


def _access_point() -> dict:
    """uap: not a switch, must be excluded by select_switches()."""
    return {
        "type": "uap",
        "name": "Living Room Wall",
        "model": "UHDIW",
        "mac": AP_MAC,
        "port_table": [],
    }


@pytest.fixture
def shop_switch() -> dict:
    return copy.deepcopy(_shop_switch())


@pytest.fixture
def us8p60_switch() -> dict:
    return copy.deepcopy(_us8p60())


@pytest.fixture
def udm_pro() -> dict:
    return copy.deepcopy(_mello_home_udm())


@pytest.fixture
def access_point() -> dict:
    return copy.deepcopy(_access_point())


@pytest.fixture
def sample_devices(shop_switch, us8p60_switch, udm_pro, access_point) -> list[dict]:
    """A realistic mixed device list: 2 usw, 1 udm, 1 uap (non-switch)."""
    return [shop_switch, us8p60_switch, udm_pro, access_point]


@pytest.fixture
def raw_stat_device_response(sample_devices) -> dict:
    """Shape of the raw UniFi controller response: {"data": [...]}."""
    return {"data": sample_devices}
