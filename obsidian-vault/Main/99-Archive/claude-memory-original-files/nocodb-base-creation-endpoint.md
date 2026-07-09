---
name: NocoDB base creation endpoint
description: Correct endpoint for creating new NocoDB bases via API (v2 workspace path)
type: reference
---

POST /api/v2/meta/workspaces/<workspace_id>/bases is the correct endpoint to create a NocoDB base. Bare /api/v2/meta/bases POST returns 403 even with a super-admin token.

Why: NocoDB v2 scopes base creation to workspaces. The bare endpoint exists only for read.

How to apply: From host (not via nocodb.synai.ai, which is Cloudflare-Access gated), use http://localhost:8090 with xc-token. Find workspace_id via GET /api/v1/workspaces. The 'Default Workspace' (we5m18cu) is owned by automations@synai.ai (org-level-creator + super). Bootstrap then proceeds via POST /api/v2/meta/bases/<base_id>/tables for each table.
