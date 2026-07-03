"""Per-port byte-counter delta -> bps conversion. PURE (no I/O, no globals).

Uses time.monotonic() by default so wall-clock/NTP jumps never produce a
bogus rate. The `now` parameter exists purely for testability.
"""
from __future__ import annotations

import time


def compute_bps(prev_bytes: int | None, curr_bytes: int, elapsed_s: float) -> int:
    """Convert a byte-counter delta into a bytes-per-second rate.

    Returns 0 (never raises, never guesses) for every edge case:
    - `prev_bytes is None`      -> first observation, no baseline yet.
    - `elapsed_s <= 0`          -> guards divide-by-zero / clock-not-advanced.
    - `curr_bytes < prev_bytes` -> counter reset (switch reboot / 32-bit wrap).
    """
    if prev_bytes is None:
        return 0
    if elapsed_s <= 0:
        return 0
    if curr_bytes < prev_bytes:
        return 0
    return int((curr_bytes - prev_bytes) / elapsed_s)


class DeltaTracker:
    """Tracks prior (rx_bytes, tx_bytes, timestamp) per (mac, port_idx).

    State is never mutated in place -- each `sample()` call rebuilds the
    internal mapping as a new dict, per the project's immutability rule.
    """

    def __init__(self) -> None:
        self._state: dict[tuple[str, int], tuple[int, int, float]] = {}

    def sample(
        self,
        mac: str,
        port_idx: int,
        rx_bytes: int,
        tx_bytes: int,
        now: float | None = None,
    ) -> tuple[int, int]:
        """Record a new sample for (mac, port_idx) and return (rx_bps, tx_bps)."""
        if now is None:
            now = time.monotonic()

        key = (mac, port_idx)
        prev = self._state.get(key)

        if prev is None:
            rx_bps, tx_bps = 0, 0
        else:
            prev_rx, prev_tx, prev_ts = prev
            elapsed = now - prev_ts
            rx_bps = compute_bps(prev_rx, rx_bytes, elapsed)
            tx_bps = compute_bps(prev_tx, tx_bytes, elapsed)

        self._state = {**self._state, key: (rx_bytes, tx_bytes, now)}
        return rx_bps, tx_bps
