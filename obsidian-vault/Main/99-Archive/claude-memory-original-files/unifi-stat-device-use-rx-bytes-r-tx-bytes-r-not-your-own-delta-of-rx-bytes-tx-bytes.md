---
name: UniFi stat/device: use rx_bytes-r/tx_bytes-r, not your own delta of rx_bytes/tx_bytes
description: Cumulative UniFi port byte counters only refresh on the device's own inform cycle (tens of seconds), so a fast self-computed delta reads mostly 0 with fake spikes -- use UniFi's own precomputed rate fields instead
type: feedback
---

UniFi Network API (stat/device) gotcha discovered debugging unifi-vision (2026-07-03):
The cumulative rx_bytes/tx_bytes counters in a switch's port_table only update once per that DEVICE's own controller-inform cycle (see device-level 'next_interval' field, commonly 30-60s), NOT on every REST poll. If you delta these cumulative counters yourself on a faster poll cadence (e.g. every 5s), the computed rate reads 0 almost every cycle and then spikes to an artificially inflated number whenever a fresh inform lands — even for a port with real, continuous traffic. This looks exactly like 'switch X isn't showing traffic' when in fact the switch has plenty.

Fix: UniFi's controller ALREADY computes a correct, continuously-fresh per-port rate — use port_table[].rx_bytes-r / tx_bytes-r / bytes-r (float, bytes/sec) directly instead of doing your own delta-over-poll-interval math on rx_bytes/tx_bytes. This eliminates an entire class of stale-counter bugs and removes the need for any client-side rate-tracking state (no monotonic timers, no counter-reset handling, no per-port state dict).

Why: found by comparing raw stat/device output for a switch with real live traffic (confirmed via rx_bytes-r) against our own computed rx_bps which was reading 0 on 3 of 4 consecutive 5s polls. General rule for any future UniFi Network API integration: prefer the '-r' rate fields UniFi already ships over computing your own deltas of the cumulative counters.
