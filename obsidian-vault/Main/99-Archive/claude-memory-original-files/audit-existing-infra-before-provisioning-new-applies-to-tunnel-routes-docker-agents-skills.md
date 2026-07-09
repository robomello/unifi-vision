---
name: Audit existing infra before provisioning new — applies to tunnel routes, Docker, agents, skills
description: Before adding a Cloudflare tunnel route / Docker service / agent / skill, grep the running system for existing equivalents. Repurpose > duplicate.
type: feedback
---

Before provisioning new infrastructure of any kind (Cloudflare Tunnel route, Docker service, agent file, skill, n8n workflow, MCP server), audit what already exists.

Minimum checks before "let's build X":
- `docker ps -a | grep -i <kw>` — is there already a container, even if not running?
- `curl ... /cfd_tunnel/$TUNNEL_ID/configurations | jq` — is there already a route?
- `ls ~/.claude/agents/ ~/skills/ | grep -i <kw>` — is there already a wrapper?
- `grep -ril <kw> ~/commander/tools ~/commander/projects` — is there already a script?

**Why:** On 2026-05-23 I built a parallel noVNC + tunnel route (`fbrefresh.synai.ai` → `localhost:6080`) for an interactive FB-cookie-refresh flow. Both pieces were wrong:
1. A `novnc` container + `vnc.synai.ai` route already existed in the tunnel ingress (route active even though the container was stopped) — would have been the right thing to revive instead of duplicating.
2. The new route used `localhost:6080`, but cloudflared runs in a container, so `localhost` = the cloudflared container, not the host. Every existing route in the ingress uses either a Docker service name (`http://novnc:6080`) or `host.docker.internal:<port>` (`ssh://host.docker.internal:22`). Looking at any sibling entry would have caught this.

**How to apply:**
- Any time you're about to provision new infra, FIRST grep/curl the current state. Quote the existing entries you're working alongside so you don't drift into incompatible patterns.
- Cloudflared specifically: tunnel `service` URLs are resolved from INSIDE the cloudflared container. Never `localhost`. Use `host.docker.internal:<port>` for host-bound processes, or a Docker service hostname for containerized targets.
- This generalizes Rule 6 (verify-before-claiming-non-existence in `~/.claude/rules/agent-behavior.md`): "verify before BUILDING new" is the same discipline applied to construction, not just refusal.
