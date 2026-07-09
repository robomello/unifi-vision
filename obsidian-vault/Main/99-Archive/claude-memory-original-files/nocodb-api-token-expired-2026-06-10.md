---
name: NocoDB API token expired (2026-06-10)
description: NOCODB_API in ~/.env returns 401; nocodb-agent broken until token regenerated
type: project
---

NOCODB_API token in ~/.env is expired/invalid (discovered 2026-06-10; all API calls return 401/403). nocodb-agent is non-functional until Roberto regenerates a token in the NocoDB UI (https://nocodb.synai.ai -> account settings -> API tokens) and updates NOCODB_API in ~/.env.
