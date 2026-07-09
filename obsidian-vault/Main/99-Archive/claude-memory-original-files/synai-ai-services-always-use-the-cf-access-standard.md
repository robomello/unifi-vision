---
name: synai.ai services: always use the CF Access standard
description: When deploying any new public *.synai.ai service, gate it with Cloudflare Access copied from nocodb.synai.ai — don't ask, don't invent a custom auth
type: feedback
---

When adding **any** new public `*.synai.ai` service, gate it with Cloudflare Access by replicating the standard already in use on the other synai.ai apps. Do not ask which auth method, do not propose in-app OAuth, do not invent a one-off config.

**Why:** Roberto explicitly said "same as others websites. this should standard" when adding Google login to activity.synai.ai. He treats CF Access + Google IdP as the house standard for these subdomains. Asking "which method" or proposing alternatives wastes his time.

**How to apply:**
1. Use the `cloudflare-agent` to do the work (it has the API token and pattern knowledge).
2. Tell it to use `nocodb.synai.ai` as the reference Access app (App ID `<REDACTED-UUID-35>`).
3. Reuse exactly: Google IdP `<REDACTED-UUID-9>`, the "Allow Roberto" policy with the same 4 allowed emails (`mello_roberto@hotmail.com`, `robomello79@gmail.com`, `vigiadoedital@gmail.com`, `engantoniogoulart@gmail.com`), 24h session, App Launcher visible, path `/*`.
4. Cloudflare team domain: `home-server-mello.cloudflareaccess.com`.
5. Verify with `curl -I https://<host>/` — should return 302 to `cloudflareaccess.com/cdn-cgi/access/login/...`.
6. Do **not** modify the tunnel ingress rule that's already in place; CF Access stacks on top of the existing tunnel route.

If the cloudflare-agent reports the existing apps don't match this pattern (e.g. the standard changed), STOP and ask — don't invent a new standard.
