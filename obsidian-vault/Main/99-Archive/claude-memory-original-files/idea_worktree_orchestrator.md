---
name: Worktree Orchestrator Plugin Idea
description: Plugin concept for managing git worktrees with Claude Code sessions -- isolated branches, tmux spawning, autonomous mode, browser support
type: project
---

Plugin idea: unified CLI for orchestrator/worker workflow using git worktrees.

**Commands:**
- `/worktree:new "feature-name" [--auto] [--chrome] [--team]` -- create isolated worktree, copy configs, install deps, spawn Claude in tmux
- `/worktree:resume "feature-name"` -- restore previous Claude session (--resume)
- `/worktree:list` -- all worktrees with branch info, uncommitted changes, commits ahead
- `/worktree:commit` -- stage and commit from orchestrator or inside worktree
- `/worktree:merge [--dry-run]` -- merge completed branches back to main, skip uncommitted, stop on conflicts
- `/worktree:removeall` -- cleanup with unmerged/uncommitted warnings

**Flags:**
- `--auto` -- Claude runs with --dangerously-skip-permissions (fully autonomous)
- `--chrome` -- spawns browser alongside Claude for frontend/visual work
- `--team` -- tmux session for multi-agent collaboration within the worktree

**Builds on:** existing `using-git-worktrees` skill, `EnterWorktree`/`ExitWorktree` tools, clawteam plugin (merge.py, cleanup-worktrees.py, tmux spawning). Metadata tracked in `.worktrees/.meta/<name>.json`.

**Why:** Full plan was drafted at `~/.claude/plans/silly-cooking-spark.md` with 16-file structure, 6 commands, 7 scripts. Ready to build whenever.

**How to apply:** When Roberto decides to build this, reference the plan file for the complete architecture. Key decision: tmux for remote access, fork clawteam scripts for individual (non-team) use.
