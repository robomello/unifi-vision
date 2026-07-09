---
name: Tunnel Network Requirement
description: Docker services needing Cloudflare Tunnel access must join n8n-net network
type: feedback
originSessionId: <REDACTED-UUID-17>
---
Any Docker service exposed via Cloudflare Tunnel must be on the `n8n-net` Docker network.

**Why:** The `cloudflared` container lives on `n8n-net`. If a service is only on its own compose-default network, cloudflared can't resolve or reach it, causing 502 Bad Gateway.

**How to apply:** When adding tunnel routes for new services (or debugging 502s), ensure the target container's docker-compose.yml includes:
```yaml
networks:
  - default
  - n8n-net

networks:
  n8n-net:
    external: true
```
