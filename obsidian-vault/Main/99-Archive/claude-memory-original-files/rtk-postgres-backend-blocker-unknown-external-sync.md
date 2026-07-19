---
name: RTK Postgres Backend — Blocker: Unknown External Sync
description: Plan to add Postgres storage backend to rtk CLI; critical blocker identified: external sync source unidentified
type: project
---

## Project: RTK Postgres Storage Backend
**Status**: Planned with critical blocker (2026-07-19)

### Scope
Add native Postgres write/read backend to rtk CLI, selected at runtime via `RTK_DATABASE_URL` env var. Preserve byte-for-byte SQLite behaviour when unset.

### Phase 0 Prerequisites (All Verified)
- **RTK version**: 0.42.4 (installed binary, source match)
- **SQLite backend**: ~/.local/share/rtk/history.db (3.9 MB)
- **Postgres target**:
  - Container: n8n-postgres
  - Connection: 127.0.0.1:5432, database `rtk`, user `n8n`
  - URL: `postgres://n8n:n8n@127.0.0.1:5432/rtk`
- **Schema**: `commands` table (2541 rows, actively updated, latest timestamp 2026-07-19), `parse_failures` (72 rows)
- **Call-site safety**: existing error handling swallows tracking failures; no `unwrap()`/`panic!` on hot path required
- **Env wiring**: `RTK_DATABASE_URL` not currently set; requires ~/.bashrc + ~/.profile configuration

### 🚨 CRITICAL BLOCKER (§0.8): Unknown External Sync Mechanism
**Finding**: Postgres `rtk` database is **already receiving updates** (2541 rows with current timestamps as of 2026-07-19) but the sync source is **unidentified**. Not found in cron, systemd --user, hooks, or scripts.

**Hypothesis**: n8n workflow or MCP tool performing out-of-band synchronization.

**Risk**: Enabling native rtk→Postgres writes while existing sync continues → potential double-writes, data divergence, inconsistent state.

**Required action**: Identify external sync source and halt it or establish write coordination before proceeding with native Postgres backend.

**Plan document**: /home/mello/.claude/plans/rtk-postgres-backend.md (Phase 0 research documented)