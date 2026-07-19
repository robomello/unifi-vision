---
name: RTK Postgres Backend Implementation
description: Phase 0 findings for native Postgres backend; critical blocker on existing sync mechanism
type: project
---

Plan: Add Postgres backend to rtk via RTK_DATABASE_URL env var; preserve SQLite when unset. Phase 0 verified 2026-07-19.

Target: n8n-postgres localhost:5432, user/pass n8n/n8n, database rtk (already 2541 rows). SQLite: ~/.local/share/rtk/history.db. Key finding: PG 'model' column is external enrichment; native inserts leave NULL.

🚨 Blocker: Existing SQLite→PG sync source unknown (not in cron/systemd/hooks). Must resolve to avoid duplicates before Phase 1.