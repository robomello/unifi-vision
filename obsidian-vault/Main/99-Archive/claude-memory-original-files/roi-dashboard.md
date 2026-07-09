---
name: roi-dashboard
description: Claude Code ROI Dashboard -- skill, CLI tool, and web dashboard at roi.synai.ai tracking all Claude activity vs senior dev cost
type: reference
---

**Repo**: https://github.com/robomello/claude-code-roi (public)

**Locations**:
- Skill + CLI: `/home/mello/skills/cost-estimate/` (cloned from GitHub)
- Dashboard: `/data/sites/roi/` (symlink to `skills/cost-estimate/dashboard/`)
- URL: https://roi.synai.ai (Cloudflare tunnel -> roi-static:8040 on n8n-net)

**Docker**: `roi-static` container, image `roi-dashboard`, needs:
- `-e HOME=/home/mello -e ROI_SCRIPT=/home/mello/skills/cost-estimate/roi.py`
- `-v /data/sites/roi:/app -v /home/mello:/home/mello:ro`
- Image built from `dashboard/Dockerfile` (python:3.12-slim + git + safe.directory=*)

**Data sources**:
- Git commits (all-time, from Co-Authored-By tags)
- `~/.claude/stats-cache.json` (tokens, daily activity -- only since Mar 14, 2026)
- `~/.claude/projects/**/*.jsonl` (session time, tool usage with --full)
- `~/.claude/projects/**/subagents/` (agent counts)
- `~/.claude/file-history/` (non-git file edits)

**Key limitation**: Session JSONL data was pruned to 5 days by `~/.claude/cleanup-sessions.sh` cron (now disabled 2026-03-30). Token/model data before Mar 14 is permanently lost.

**Cleanup cron disabled**: Removed from crontab on 2026-03-30 so session data accumulates going forward. Script still exists at `~/.claude/cleanup-sessions.sh` but won't run.
