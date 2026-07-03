"""Unit tests for filter.py — select configured switches from stat/device (PURE)."""
from __future__ import annotations

from filter import normalize_mac, select_switches

from conftest import AP_MAC, SHOP_SWITCH_MAC, UDMPRO_MAC, US8P60_MAC


class TestNormalizeMac:
    def test_lowercases(self):
        assert normalize_mac("AA:BB:CC:11:22:33") == "aabbcc112233"

    def test_strips_colons(self):
        assert normalize_mac("aa:bb:cc:11:22:33") == "aabbcc112233"

    def test_strips_dashes(self):
        assert normalize_mac("aa-bb-cc-11-22-33") == "aabbcc112233"

    def test_already_normalized(self):
        assert normalize_mac("aabbcc112233") == "aabbcc112233"


class TestSelectSwitches:
    def test_empty_allowlist_returns_all_usw_and_udm(self, sample_devices):
        result = select_switches(sample_devices, switch_macs=None)
        macs = {d["mac"] for d in result}
        assert macs == {SHOP_SWITCH_MAC, US8P60_MAC, UDMPRO_MAC}

    def test_empty_string_switch_macs_returns_all(self, sample_devices):
        result = select_switches(sample_devices, switch_macs="")
        macs = {d["mac"] for d in result}
        assert macs == {SHOP_SWITCH_MAC, US8P60_MAC, UDMPRO_MAC}

    def test_non_switch_device_excluded(self, sample_devices):
        result = select_switches(sample_devices, switch_macs=None)
        assert all(d["type"] in ("usw", "udm") for d in result)
        assert AP_MAC not in {d["mac"] for d in result}

    def test_mac_allowlist_intersects(self, sample_devices):
        result = select_switches(sample_devices, switch_macs=[SHOP_SWITCH_MAC])
        assert len(result) == 1
        assert result[0]["mac"] == SHOP_SWITCH_MAC

    def test_mac_allowlist_case_and_separator_insensitive(self, sample_devices):
        weird_case = SHOP_SWITCH_MAC.upper().replace(":", "-")
        result = select_switches(sample_devices, switch_macs=[weird_case])
        assert len(result) == 1
        assert result[0]["mac"] == SHOP_SWITCH_MAC

    def test_mac_allowlist_multiple_entries(self, sample_devices):
        result = select_switches(sample_devices, switch_macs=[SHOP_SWITCH_MAC, UDMPRO_MAC])
        macs = {d["mac"] for d in result}
        assert macs == {SHOP_SWITCH_MAC, UDMPRO_MAC}

    def test_mac_allowlist_no_match_returns_empty(self, sample_devices):
        result = select_switches(sample_devices, switch_macs=["11:11:11:11:11:11"])
        assert result == []

    def test_comma_separated_string_allowlist(self, sample_devices):
        macs_csv = f"{SHOP_SWITCH_MAC},{US8P60_MAC}"
        result = select_switches(sample_devices, switch_macs=macs_csv)
        macs = {d["mac"] for d in result}
        assert macs == {SHOP_SWITCH_MAC, US8P60_MAC}

    def test_empty_devices_list_returns_empty(self):
        assert select_switches([], switch_macs=None) == []

    def test_malformed_device_missing_type_skipped(self, sample_devices):
        malformed = {"name": "no type field", "mac": "ff:ff:ff:ff:ff:ff"}
        result = select_switches(sample_devices + [malformed], switch_macs=None)
        assert "ff:ff:ff:ff:ff:ff" not in {d.get("mac") for d in result}

    def test_malformed_device_missing_mac_skipped_when_allowlist_active(self, sample_devices):
        malformed = {"type": "usw", "name": "no mac field"}
        result = select_switches(sample_devices + [malformed], switch_macs=[SHOP_SWITCH_MAC])
        assert all(d.get("mac") for d in result)

    def test_non_dict_entry_in_devices_list_skipped(self, sample_devices):
        result = select_switches(sample_devices + [None, "garbage", 42], switch_macs=None)
        macs = {d["mac"] for d in result}
        assert macs == {SHOP_SWITCH_MAC, US8P60_MAC, UDMPRO_MAC}

    def test_does_not_mutate_input_devices_list(self, sample_devices):
        original_len = len(sample_devices)
        original_ids = [id(d) for d in sample_devices]
        select_switches(sample_devices, switch_macs=[SHOP_SWITCH_MAC])
        assert len(sample_devices) == original_len
        assert [id(d) for d in sample_devices] == original_ids
