---
name: activity.synai.ai — personal activity tracker
description: Single-user mobile-first activity tracker at activity.synai.ai. FastAPI + Postgres, port 8076, CF Access gated
type: project
---

Personal activity tracker for logging how Roberto spends his day (built 2026-05-02).

**Live URL:** https://activity.synai.ai (CF Access gated — Google login, 4-email allowlist via the "Allow Roberto" policy reused from nocodb).

**Source:** `/home/mello/commander/projects/activity-tracker/` (FastAPI + asyncpg + Jinja2; vanilla HTML/CSS/JS frontend).
**Container:** `activity-tracker` on `127.0.0.1:8076`, network `n8n-net`, defined in `/home/mello/docker-compose.yml`.
**Database:** Postgres `activity` on the existing `n8n-postgres` container (auto-created on first start). Tables: `activities` (button list, soft-delete via `active`) and `activity_log` (start_time, end_time, activity_name, notes — UTC stored, UTC-6 rendered via `APP_TZ_OFFSET_HOURS=-6`).
**Tunnel:** `activity.synai.ai` → `http://activity-tracker:8076` on tunnel `<REDACTED-UUID-2>`.
**CF Access app ID:** `<REDACTED-UUID-3>` (created from the nocodb template).

**Why:** Roberto wanted a one-tap mobile UI to track time per activity (Computer / Walk / Printer / Eat / Yard / Family / Sleep / Other) and compare against recovery goals. Tapping a button auto-stops the previous activity. Has Today (totals + timeline), History (7-day stacked bar), and Settings (button management) views.

**How to apply:** When the user asks about "the activity tracker" or wants to extend it (new view, new metric, export, integration), this is the project. Reuse the existing FastAPI app and Postgres schema; don't spin up a new service. The button list is editable from the Settings tab in the app itself, not via code/env vars.
