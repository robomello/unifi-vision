"""Select configured switches from a raw stat/device list. PURE (no I/O).

Named `filter.py` per the implementation plan. Import it explicitly
(`from filter import select_switches`) -- inside this package it never
collides with the builtin `filter()`, since Python only shadows builtins
for unqualified names inside this module's own top-level scope, and this
module does not call the builtin `filter()` anywhere.
"""
from __future__ import annotations

import re
from collections.abc import Iterable

SWITCH_TYPES = frozenset({"usw", "udm"})

_NON_MAC_CHARS = re.compile(r"[^0-9a-f]")


def normalize_mac(mac: str) -> str:
    """Lowercase and strip separators so MACs compare equal regardless of format."""
    return _NON_MAC_CHARS.sub("", mac.lower())


def _parse_allowlist(switch_macs: str | Iterable[str] | None) -> frozenset[str] | None:
    """Build a normalized MAC allowlist. Returns None when no filtering applies."""
    if switch_macs is None:
        return None
    if isinstance(switch_macs, str):
        raw_macs = [m for m in switch_macs.split(",") if m.strip()]
    else:
        raw_macs = [m for m in switch_macs if m]
    if not raw_macs:
        return None
    return frozenset(normalize_mac(m) for m in raw_macs)


def select_switches(devices: Iterable, switch_macs: str | Iterable[str] | None = None) -> list[dict]:
    """Return the subset of `devices` that are switches (usw/udm), optionally
    intersected with a MAC allowlist. Never raises on malformed entries --
    non-dict items and dicts missing expected keys are silently skipped.
    """
    allowlist = _parse_allowlist(switch_macs)
    result: list[dict] = []

    for device in devices:
        if not isinstance(device, dict):
            continue
        if device.get("type") not in SWITCH_TYPES:
            continue
        if allowlist is not None:
            mac = device.get("mac")
            if not mac or normalize_mac(mac) not in allowlist:
                continue
        result.append(device)

    return result
