---
name: git-config
description: Git repo config for ~/.claude -- push to otto remote (claude-brain), branch backup/mello-server
type: reference
---

The `~/.claude` directory is a git repo with two remotes:

- **origin**: `https://github.com/robomello/claude-config.git` (NOT used for pushing)
- **otto**: `https://github.com/robomello/claude-brain.git` (shared repo between both servers)

**Two servers**: Mello (this server) and Otto (the other server). Both push to `claude-brain`.

**Push target**: `otto` remote, `main` branch.
- Mello-server configs: `machines/mello-server/`
- Otto-server configs: `machines/otto-server/`
- Shared configs: `shared/`

```bash
git push otto main
```

**Repo structure**: Root-level dirs (`/agents/`, `/hooks/`, `/rules/`, etc.) are gitignored -- deployed by `sync.py` from `shared/` and `machines/`. Canonical source is always `shared/` or `machines/mello-server/`.

**Memory files** (`projects/-home-mello/memory/`) are gitignored -- synced to PostgreSQL via `memory_sync.py` cron instead.
