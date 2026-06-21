# OTTO / Claude Code — Milestones

Evidence-based timeline, reconstructed from git history, file timestamps, PRDs, and the Obsidian vault on the home server (2026-06-21). Dates marked **[exact]** come from a commit or document; **[file mtime]** from earliest preserved artifact; **[bounded]** where the precise day isn't recorded here and the real source is on the Mercedes server.

## Phase 0 — AI vetting (pre-OTTO)
- **Years prior** — long private vetting: equipment bought, new LLMs run against a wall of tests before any production trust. (Not dated in these trees.)
- **2025-12-29 [file mtime]** — earliest Claude Code artifact on disk (ralph-wiggum plugin). Claude Code experimentation underway.

## Phase 1 — OTTO v2 stood up at Mercedes (Jan 2026)
- **2026-01-13 [file mtime]** — OTTO v2 codebase scaffolded (README created).
- **2026-01-19 [file mtime]** — **OTTO database initialized** (`init_db.sql`, `phase8b_migration.sql`). Server/DB stood up. This is the best on-box proxy for "server started at Mercedes."
- **2026-01-20 [file mtime]** — first `.claude/` agents created (database, fastapi, security).
- **2026-01-30 [exact]** — `otto.prd.md` declares status **Active/Production**. OTTO v2 is live by this date.
- **OTTO first reply** — *not retrievable from this box.* Lives in OTTO's Postgres on corpintra. See "How to fill the gaps" below.

## Phase 2 — Config formalized + brain build-out (Feb–Mar 2026)
- **2026-02-02 [exact]** — Claude Code configuration put under version control ("track Claude Code configuration").
- **2026-03-03 [file mtime]** — orchestrator agent added.
- **2026-03-13 [exact]** — OTTO Claude configuration committed; plan-agent improvements begin.
- **2026-03-21 [exact]** — cloudflare-agent baseline; self-improvement loop starts.
- **2026-03-22 [exact]** — full brain export (agents, skills, hooks, rules, soul, memory); cross-pollination Otto <-> home.
- **2026-03-23 [exact]** — `claude-brain` repo initialized.

## Phase 3 — Production features + leadership exposure (Apr 2026)
- **2026-04-21 [vault]** — OTTO presented to Michael Bauer. 5 engineers using it daily.
- **2026-04-23 [exact]** — OEE charts migrated to traffic-light (yellow/red/green) colors.
- **2026-04-24 [exact]** — Paint Shop (OF) support added; tabbed Table/Chart multi-line OEE.
- **2026-04-27 [exact]** — last push to develop branch (KPI renderers, area tools, briefing service, spot repair).

## Phase 4 — Hardware scale-up (Jun 2026)
- **2026-06-13 [vault]** — plan to move both home-server GPUs to Mercedes.
- **2026-06-14 [vault]** — physical GPU migration executed (both RTX PRO 6000s -> baby-otto).
- **2026-06-18 [vault]** — OTTO confirmed no longer air-gapped (outbound internet).
- **2026-06-19 [vault]** — 4x RTX PRO 6000 Blackwell GPUs confirmed at OTTO.
- **2026-06-20 [vault]** — new OTTO server IP 10.49.50.254 confirmed.

---

## How to fill the two gaps (run on the Mercedes / OTTO server)

**Exact server go-live** (first time the app/DB actually came up):
```bash
# earliest row in any audit/login table, and DB creation time
psql -d otto -c "SELECT min(created_at) AS db_first_event FROM login_events;"
psql -d otto -c "SELECT min(created_at) FROM conversations;"
```

**OTTO's first reply** (first assistant message ever):
```bash
psql -d otto -c "SELECT created_at, role, left(content, 120) FROM messages WHERE role='assistant' ORDER BY created_at ASC LIMIT 1;"
# (adjust table/column names to OTTO's actual schema in init_db.sql)
```

Bring those two timestamps back and this file becomes complete.
