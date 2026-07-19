---
name: Always recreate Docker containers, never restart to pick up changes
description: Standing rule: recreate Docker containers fresh, never restart/reuse to pick up changes
type: feedback
---

Roberto's standing rule for all Docker work: never restart or reuse a stale container to pick up config/code/image changes. Always recreate fresh with `docker compose up -d --force-recreate` (or `down` + `up`), never a bare `restart`/`start`. Treat running containers as disposable — persistence lives ONLY in named volumes, never in container state. (Corrective feedback given during crm.synai.ai / twenty-crm Google OAuth debugging.)
