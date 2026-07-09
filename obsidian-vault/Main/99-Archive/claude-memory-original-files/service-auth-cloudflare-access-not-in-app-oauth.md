---
name: Service auth = Cloudflare Access, not in-app OAuth
description: Home-server public services are gated by Cloudflare Access (edge Google login), not in-app auth; replicate via cloudflare-agent
type: reference
---

All public-facing services on the home server (synai.ai subdomains AND drinkwaretrove.com) are gated by **Cloudflare Access** applications at the edge: Google login via `home-server-mello.cloudflareaccess.com`, restricted by per-app email policies. There is NO in-app auth code.

When asked to add login/auth/OAuth to a service here, replicate the Cloudflare Access pattern using the `cloudflare-agent`. Do NOT build NextAuth or in-app auth.

- Manage via the Cloudflare API; token/account in `/home/mello/.env` (`CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID`). The `cloudflare-agent` has the exact REST recipes for apps/policies.
- Free plan caps 4 destinations per Access app; use multiple apps for more paths.
- drinkwaretrove.com admin (set up 2026-05-18): apps "Drinkware Trove Admin" + "Drinkware Trove Admin API" gate /studio, /review, /benchmark, /api/review, /api/benchmark, /api/templates. Policy "Allow Roberto" = mello_roberto@hotmail.com + robomello79@gmail.com. The public mug gallery stays ungated.
- After putting CF Access in front of a path, remove any redundant in-app gate (drinkwaretrove's old middleware.js STUDIO_SECRET) or it will 401 authenticated users.
