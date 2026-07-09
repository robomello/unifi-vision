---
name: Quarterly Maintenance
description: quarterly-maintenance.sh script at ~/.claude/scripts/ -- audits agent descriptions, naming, duplicates, bloat, CLAUDE.md sync, registry freshness
type: reference
---

# Quarterly Maintenance Script

**Location**: `~/.claude/scripts/quarterly-maintenance.sh`
**Created**: 2026-03-30

Audits 6 areas:
1. Agent descriptions -- checks for trigger patterns (Use when / ALWAYS use / Triggers on / Use PROACTIVELY)
2. Naming consistency -- flags snake_case agent filenames (should be kebab-case)
3. Archived duplicates -- byte-diffs active vs _archived/ agents
4. Plan/todo/context accumulation -- counts and sizes with thresholds
5. CLAUDE.md sync -- checks root vs .claude/ versions, agent count accuracy
6. Agent registry freshness -- compares README.md timestamp vs newest agent

**Known fix**: Original version used `((VAR++))` which fails under `set -e` when VAR is 0. Fixed to `VAR=$((VAR + 1))` on 2026-03-30.

**Schedule**: Not yet in cron. Recommended: 1st of Jan/Apr/Jul/Oct at 6 AM.

## Memory Audit Cron

**Location**: `~/.claude/memory-audit-cron.sh`
**Schedule**: Every other day at 12:34 AM CT (`34 0 */2 * *`). Changed from weekly Sundays 8:03 AM on 2026-04-04.

## Stale Memory Detection Hook

**Location**: `~/.claude/hooks/stale-memory-check.sh`
**Hook type**: SessionStart (informational, never blocks)
**What it does**: Finds memory files older than 30 days, outputs warning with count and names. Created 2026-04-04.
