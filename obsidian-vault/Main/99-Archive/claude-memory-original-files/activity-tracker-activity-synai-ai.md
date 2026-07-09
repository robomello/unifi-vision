---
name: Activity Tracker (activity.synai.ai)
description: Personal daily-activity tracker — FastAPI + Postgres at activity.synai.ai / activity-tracker:8076
type: reference
---

Personal daily-activity tracker. Single-user web app where Roberto logs time spent on activities by tapping a button to switch.

**Where it lives**
- Code: `/home/mello/commander/projects/activity-tracker/` (`app.py`, `Dockerfile`, `templates/`, `static/`)
- Container: `activity-tracker` (from docker-compose.yml)
- Port: `127.0.0.1:8076` -> tunnel `activity.synai.ai`
- Database: Postgres `n8n@postgres:5432/activity` (separate `activity` DB, auto-created on boot)
- Timezone: UTC-6 (`APP_TZ_OFFSET_HOURS=-6`)

**Data model**
- `activities(id, name, display_order, active, created_at)` — defaults: Computer, Walk, Printer, Eat, Yard, Family, Sleep, Other
- `activity_log(id, activity_name, start_time, end_time, notes, latitude, longitude, accuracy_m)` — open entry has `end_time IS NULL`

**API (FastAPI)**
- `GET /api/state` — current open activity + active list
- `POST /api/switch` `{activity_name, notes?, location?}` — closes any open entry, opens new one. **Always uses `now()` — does NOT accept a custom start_time.**
- `POST /api/stop` — closes any open entry (idle gap)
- `PATCH /api/log/{id}` — patch `latitude/longitude/accuracy_m/notes` only (no time fields exposed)
- `POST /api/undo` — undo last switch (delete + reopen prior) or last stop (clear end_time)
- `GET /api/today` / `GET /api/history` / `GET /api/activities`
- CRUD on activities: `POST/PUT/DELETE /api/activities[/id]`, `POST /api/activities/reorder`
- `GET /healthz`

**How to backdate or edit times**
The HTTP API does not expose `start_time` / `end_time` for editing. To backdate or correct entries, write directly to Postgres:
```bash
docker exec -it n8n-postgres psql -U n8n -d activity -c \
 "INSERT INTO activity_log (activity_name, start_time, end_time, notes) VALUES ('Yard', '2026-05-04 16:00-06', '2026-05-04 18:45-06', 'note');"
```
Or `UPDATE activity_log SET start_time = ..., end_time = ... WHERE id = ...;`

**Why this memory exists**
On 2026-05-04 Claude searched only Obsidian for "activity page" and claimed nothing existed. Roberto corrected: the app is at `commander/projects/activity-tracker`. Lesson: when Roberto says "my X" and X isn't found, also grep `commander/projects/`, `docker-compose.yml`, and `~/.claude/agents/` before claiming it doesn't exist.
