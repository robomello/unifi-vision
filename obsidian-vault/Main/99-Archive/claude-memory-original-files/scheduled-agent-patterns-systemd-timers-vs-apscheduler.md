---
name: Scheduled Agent Patterns (Systemd Timers vs APScheduler)
description: Two scheduling systems used on the home server, when to pick each, etsy-competitor-tracker as canonical systemd exemplar
type: reference
---

# Scheduled Agent Patterns on Mello Server

Mello's environment uses **two complementary scheduling systems** for agents:

## 1. Systemd User Timers (Recommended for Standalone Agents)

**Three files required:**

1. **`~/.config/systemd/user/AGENT.timer`** — schedule definition
   - `OnCalendar=hourly` | `daily` | `*-*-* 09:00:00` | `*-*-* 9,14,19:00:00`
   - `Persistent=true` so missed runs catch up after reboot
   - `WantedBy=timers.target`

2. **`~/.config/systemd/user/AGENT.service`** — execution handler
   - `Type=oneshot`
   - `WorkingDirectory=/home/mello/commander`
   - `ExecStart=/bin/bash /path/to/cron_run.sh`
   - `TimeoutStartSec=14400` (4h kill)

3. **`/home/mello/commander/projects/AGENT/cron_run.sh`** — bash wrapper
   - `flock` lock to prevent overlap (`LOCKFILE=/tmp/AGENT.lock`)
   - `timeout 300 python3 -m projects.AGENT.run`
   - Date-stamped log files in `/home/mello/logs/AGENT/`
   - `find … -mtime +30 -delete` log rotation

**Control:**
```bash
systemctl --user daemon-reload
systemctl --user enable --now AGENT.timer
systemctl --user status AGENT.timer
journalctl --user -u AGENT.service -f
```

**Live exemplar:** `etsy-competitor-tracker` — daily 09:00 UTC, files at `~/.config/systemd/user/etsy-competitor-tracker.{timer,service}`, wrapper at `/home/mello/commander/projects/etsy_competitor_tracker/cron_run.sh`. Copy this when building a new scheduled agent.

## 2. APScheduler (Commander In-Process)

In `/home/mello/commander/scheduler.py` — jobs run in Commander's event loop. Triggers:
- `IntervalTrigger(hours=1)` or `minutes=30`
- `CronTrigger(hour=14, minute=0, timezone='UTC')` for specific times
- `max_instances=1`, `misfire_grace_time=300` to avoid overlap

## Decision Rule

| Question | Use |
|---|---|
| Needs to survive Commander restarts? | Systemd timer |
| Sub-minute interval? | APScheduler |
| Standalone with its own logs/isolation? | Systemd timer |
| Already inside Commander's flow? | APScheduler |

## Currently Scheduled Agents

| Agent | Schedule | Mechanism |
|---|---|---|
| etsy-competitor-tracker | Daily 09:00 UTC | Systemd |
| Etsy cookie refresh | timer | Systemd |
| matomo-archive | Daily 07:00 UTC | Systemd |
| self-improver (eval-gen, improve) | timer | Systemd |
| post-publish-optimizer | timer | Systemd |
| Etsy sales check | hourly | APScheduler |
| Etsy sync | every 15 min | APScheduler |

## Anti-Patterns

- **Don't invoke `claude --print` from cron** for heavy-frequency runs — slow boot, API latency. Use Claude CLI only for the orchestration/planning step inside the cron script, not the loop.
- Agent definition file (`~/.claude/agents/AGENT.md`) is metadata + CLI for **manual** invocation; the cron path bypasses it.

