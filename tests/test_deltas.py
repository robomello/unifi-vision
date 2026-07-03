"""Unit tests for deltas.py — byte-counter -> bps conversion (PURE)."""
from __future__ import annotations

from deltas import DeltaTracker, compute_bps


class TestComputeBps:
    def test_normal_rate(self):
        # 1,000,000 bytes over 10s = 100,000 bytes/s
        assert compute_bps(prev_bytes=0, curr_bytes=1_000_000, elapsed_s=10) == 100_000

    def test_first_seen_no_prev_returns_zero(self):
        assert compute_bps(prev_bytes=None, curr_bytes=12345, elapsed_s=5) == 0

    def test_counter_reset_clamps_to_zero(self):
        # curr < prev -> switch rebooted / counter wrapped
        assert compute_bps(prev_bytes=5000, curr_bytes=100, elapsed_s=5) == 0

    def test_zero_elapsed_guard(self):
        assert compute_bps(prev_bytes=100, curr_bytes=200, elapsed_s=0) == 0

    def test_negative_elapsed_guard(self):
        assert compute_bps(prev_bytes=100, curr_bytes=200, elapsed_s=-3) == 0

    def test_equal_bytes_zero_rate(self):
        assert compute_bps(prev_bytes=500, curr_bytes=500, elapsed_s=5) == 0

    def test_returns_int_not_float(self):
        result = compute_bps(prev_bytes=0, curr_bytes=333, elapsed_s=10)
        assert isinstance(result, int)
        assert result == 33


class TestDeltaTracker:
    def test_first_sample_returns_zero_zero(self):
        tracker = DeltaTracker()
        rx_bps, tx_bps = tracker.sample("aa:bb", 1, rx_bytes=1000, tx_bytes=500, now=100.0)
        assert (rx_bps, tx_bps) == (0, 0)

    def test_second_sample_computes_rate(self):
        tracker = DeltaTracker()
        tracker.sample("aa:bb", 1, rx_bytes=1000, tx_bytes=500, now=100.0)
        rx_bps, tx_bps = tracker.sample("aa:bb", 1, rx_bytes=6000, tx_bytes=1500, now=105.0)
        assert rx_bps == 1000  # (6000-1000)/5
        assert tx_bps == 200  # (1500-500)/5

    def test_counter_reset_between_samples_clamps_zero(self):
        tracker = DeltaTracker()
        tracker.sample("aa:bb", 1, rx_bytes=9000, tx_bytes=9000, now=100.0)
        rx_bps, tx_bps = tracker.sample("aa:bb", 1, rx_bytes=100, tx_bytes=50, now=105.0)
        assert (rx_bps, tx_bps) == (0, 0)

    def test_different_ports_tracked_independently(self):
        tracker = DeltaTracker()
        tracker.sample("aa:bb", 1, rx_bytes=1000, tx_bytes=1000, now=100.0)
        tracker.sample("aa:bb", 2, rx_bytes=2000, tx_bytes=2000, now=100.0)
        rx1, tx1 = tracker.sample("aa:bb", 1, rx_bytes=1100, tx_bytes=1100, now=101.0)
        rx2, tx2 = tracker.sample("aa:bb", 2, rx_bytes=2500, tx_bytes=2500, now=101.0)
        assert (rx1, tx1) == (100, 100)
        assert (rx2, tx2) == (500, 500)

    def test_different_macs_same_port_idx_tracked_independently(self):
        tracker = DeltaTracker()
        tracker.sample("aa:bb", 1, rx_bytes=1000, tx_bytes=1000, now=100.0)
        tracker.sample("cc:dd", 1, rx_bytes=9000, tx_bytes=9000, now=100.0)
        rx1, _ = tracker.sample("aa:bb", 1, rx_bytes=1100, tx_bytes=1100, now=101.0)
        rx2, _ = tracker.sample("cc:dd", 1, rx_bytes=9100, tx_bytes=9100, now=101.0)
        assert rx1 == 100
        assert rx2 == 100

    def test_uses_monotonic_clock_when_now_not_supplied(self):
        tracker = DeltaTracker()
        # Should not raise, and first call is always (0, 0) regardless of clock source.
        rx_bps, tx_bps = tracker.sample("aa:bb", 1, rx_bytes=1000, tx_bytes=1000)
        assert (rx_bps, tx_bps) == (0, 0)

    def test_internal_state_not_mutated_in_place(self):
        """Sampling must produce a new state mapping, never mutate the old one."""
        tracker = DeltaTracker()
        tracker.sample("aa:bb", 1, rx_bytes=1000, tx_bytes=1000, now=100.0)
        state_ref_1 = tracker._state
        tracker.sample("aa:bb", 1, rx_bytes=2000, tx_bytes=2000, now=101.0)
        state_ref_2 = tracker._state
        assert state_ref_1 is not state_ref_2
        # And the earlier snapshot must be untouched (still holds the old sample).
        assert state_ref_1[("aa:bb", 1)] == (1000, 1000, 100.0)
