---
name: Full project means full project — never leave infra steps for the user
description: When Roberto says 'full project' or 'fully autonomous,' do not stop short on Cloudflare routes, docker-compose edits, env vars, ports, or other 'shared infra.' Use the agents (cloudflare-agent, deploy-agent, etc.). Asking him to add a route after he asked for autonomy = wasted time.
type: feedback
---

**Rule**: When Roberto says "full project", "fully autonomous", "do everything", or otherwise hands over end-to-end execution, complete every step including the infrastructure pieces (Cloudflare Tunnel routes, docker-compose entries, env-var wiring, port allocation, DNS records). Do NOT defer infra steps to him with phrases like "needs a Cloudflare Tunnel route" or "add this snippet to docker-compose.yml" unless an actual credential is missing.

**Why**: 2026-04-25 — On the TikTok Shop project, I built the FastAPI dashboard, container, NocoDB schema, and agents end-to-end, but stopped at the Cloudflare Tunnel route, telling Roberto to add it manually. He said "When I tell you do to a full project, you do the full project, cloudflare should have been done, now I am wasting time." The cloudflare-agent existed for this exact purpose; I had `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID`, and `CLOUDFLARE_ZONE_ID` already in `~/.env`. There was no real blocker — only my over-cautious read of the "destructive actions need confirmation" rule.

**How to apply**:
- "Shared infrastructure" rules in `~/.claude/rules/` are about destructive ops (deletes, force-pushes, drops). Adding a route, a service, a DNS record, or an env-var entry to Roberto's own systems while executing a project he asked for is NOT destructive — it's the work.
- Specifically for new services: when a project needs a public URL, automatically use cloudflare-agent to add the DNS CNAME + tunnel ingress rule. Don't write "Add a route at..." in a README and call it done.
- For docker-compose: if the project warrants it, append the service block. Don't leave a `.snippet.yml` for the user to merge.
- For env vars: if the project needs one and it's a config value (not a secret to obtain), set it directly.
- Only stop and ask when (a) a credential is genuinely missing, (b) the action would clobber another user's work, or (c) it would touch a system outside the current project's scope.

**Triggers that mean "do everything"**: "full project", "fully autonomous", "do everything", "make this work", "use all the tools", "use all our tools", "fire and forget", "don't ask, just do", "auto mode" (when active in the harness).

**Counter-anti-pattern check before stopping**: before adding any "Roberto needs to..." line to a README or final summary, ask whether an existing agent/tool can do that step. If yes, do it.
