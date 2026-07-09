---
name: OTTO v2 status snapshot 2026-04-27
description: OTTO v2 repo state, active phase, branch, and recent work areas as of 2026-04-27
type: project
---

OTTO v2 is well past Phase 2/3 — supersedes the older "Phase 2 done, Phase 3 waiting" note.

**Repo**: https://github.com/robomello/otto (PRIVATE). Default branch is `develop` (not `main`). Pushed last on 2026-04-27 from work before Roberto left for the day.

**Active phase**: Phase 8B (PRD `OTTO_Phase_8B_PRD_Complete.md`, 38 KB) and Phase 8C Autonomous Monitoring (PRD 46 KB) are the live design docs. Phase 3 roadmap/prep/quickstart files still sit at root as historical context. There is a `phase8b_migration.sql` plus `phase-4.sh`, `phase-5.sh`, `phase-6.sh` that were all run earlier.

**Architecture has filled out**. `app/` now includes: `agents/`, `analysis/`, `auth/`, `db/`, `harness/`, `jwt/`, `llm/`, `memory/`, `middleware/`, `monitors/`, `orchestrator/`, `prompts/`, `renderers/`, `routers/`, `schemas/`, `services/`, `tools/`, `validators/`. The orchestrator + micro-agents pattern (Classifier, iPortal, Ignition, RAG, System) from the README is the entry point but real work happens through monitors/renderers/services.

**Recent work (last week, all on develop)**:
- `f6e27fb` 2026-04-27 — store structured KPI data in `response_data` JSONB column
- `14dd54d` 2026-04-27 — KPI renderers, area tools, briefing service, spot repair, frontend updates (the big batch)
- `7d843d9` 2026-04-24 — Paint Shop (OF) support for cycle timer endpoints
- `218fb38` 2026-04-24 — tabbed Table/Chart view for multi-line OEE responses
- `a1e408b` 2026-04-23 — migrated stored OEE charts to yellow/red/green traffic-light colors

**Other notable additions** vs. old Phase 2 snapshot: `spot_repair/` module, `monitors/` (autonomous monitoring per Phase 8C), `mcp/` directory plus `.mcp.json`, `node-red-flows/`, `e2e-tests/` + `playwright.config.ts` + `playwright-bundle/`, `architecture-site/`, `migrations/`. `PRDs/` holds modular PRDs: otto, palai-llm, chromahandler, dtwv3, ocr-service, promptpower, servicemanager, sqlquerybot, aih-chatbot-template.

**Runtime gotchas (still true)**: Ollama on port **11435** (not 11434). API on 8070 prod / 8071 dev hot-reload. Ships in Docker via `docker compose up -d`.

**Tech mix**: Python-dominant (2.6 MB), TS frontend (832 KB), HTML 1.1 MB, plus Shell/PLpgSQL/RouterOS/CSS/TeX. No issues, no PRs open.

**Working dir on the work server**: still `/home/mbot/otto/` per prior memory (not re-verified this session).
