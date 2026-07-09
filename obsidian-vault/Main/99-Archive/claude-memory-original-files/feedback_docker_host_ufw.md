---
name: Docker-to-host UFW port blocking
description: When exposing host-native services to Docker containers on n8n-net, UFW blocks the port -- must add UFW rule first
type: feedback
---

When a service runs natively on the host (not in Docker) and needs to be reached from Docker containers (e.g., cloudflared on n8n-net), UFW's default DROP policy blocks the connection.

**Why:** UFW INPUT chain has `policy DROP`. Docker-published container ports bypass UFW via the DOCKER iptables chain, but host-native services go through INPUT and get dropped. This causes `i/o timeout` errors from cloudflared when trying to reach host ports.

**How to apply:** Before setting up a Cloudflare tunnel route to a host-native service:
1. Identify the port the service uses
2. Add UFW rule FIRST: `sudo ufw allow from 172.16.0.0/12 to any port <PORT> proto tcp comment "<service> from Docker"`
3. Use `host.docker.internal:<PORT>` as the tunnel target (resolves to 172.17.0.1 inside containers)
4. The `172.16.0.0/12` CIDR covers all Docker bridge networks (172.16-31.x.x)

**Anti-pattern (what I keep doing):** Try localhost, then gateway IP, then socat proxy, then finally discover UFW is blocking. Skip all that -- check UFW first.
