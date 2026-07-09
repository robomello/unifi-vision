---
name: FORGE Project
description: FORGE agent orchestration platform -- location, stack, security status, Mercedes deployment readiness
type: project
---

## FORGE -- Factory & Operations Runtime for Goal Execution

- **Location**: `/home/mello/forge/`
- **Repo**: https://github.com/robomello/forge (private)
- **Port**: 3201, domain: forge.synai.ai
- **Container**: `forge` on n8n-net, shares n8n-postgres (database: `forge`)
- **Stack**: Node.js 22, Express, PostgreSQL, React 18, Tailwind CSS, WebSocket, Vite

**What it does**: Multi-company agent orchestration. Users create companies with AI agents, define goals that decompose into tasks, execute via multiple runtimes (Claude CLI, Claude API, Bash, HTTP, n8n), track costs/budgets, approve gates, and monitor in real-time via WebSocket.

**Scale**: 62 API endpoints, 20+ DB tables, 12 background services, 20 UI pages, 6 task runtimes.

### Current state (2026-04-05)

- **Git**: Initialized with 18 commits on master, pushed to GitHub private repo
- **Tests**: 69 tests across 6 files (vitest), covering auth, validation, bash runtime, claude-cli, scheduler, costs
- **Lint**: ESLint flat config (zero errors), TypeScript JSDoc on 6 security-critical files
- **CI**: GitHub Actions (lint + test + coverage + npm audit + Trivy security scan)
- **Security**: Enterprise-hardened for Mercedes W138 deployment
  - CF Access JWT with audience validation
  - RBAC (admin/operator/viewer/auditor) with atomic first-admin provisioning
  - Helmet security headers (CSP, HSTS, referrer policy)
  - Request ID tracking for audit trail
  - Nonce XML delimiters in all runtimes (prompt injection mitigation)
  - Bash runtime deny-by-default (empty allowlist rejected)
  - SSRF protection (private IP blocklist) on HTTP runtime
  - Path traversal protection on agent_md_path
  - Docker secrets, container hardening (read-only, no-new-privileges, cap_drop ALL)
  - Atomic budget tracking (transaction-wrapped)
  - TOCTOU fix for decomposer (compareAndSetStatus)
- **Docs**: 10 compliance/deployment docs including TISAX matrix, threat model, incident response
- **Migrations pending**: 005_rbac.sql, 006_audit_enhanced.sql, 007_performance_indexes.sql

### Remaining items before Mercedes deployment

1. **Rotate Telegram bot token** (exposed in .env)
2. Run pending migrations: `npm run db:migrate:rbac`, `npm run db:migrate:audit`
3. Run performance indexes migration
4. **Anthropic DPA** must be established before processing Confidential plant data (TISAX IS-15)
5. MEDIUM: Validate companies/import body with Zod schema
6. MEDIUM: Add SSRF blocklist to n8n-webhook runtime
7. LOW: Redact agent.constraints secrets on API reads
8. LOW: Per-endpoint rate limiting on expensive operations (decompose, scheduler tick)

**How to apply:** Build/deploy via `cd /home/mello/forge && docker stop forge && docker rm forge && docker compose up -d`. Use `npm test` to verify, `npm run lint` for style.
