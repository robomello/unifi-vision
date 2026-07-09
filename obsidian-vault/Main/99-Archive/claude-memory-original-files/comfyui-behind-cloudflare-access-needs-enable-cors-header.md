---
name: ComfyUI behind Cloudflare Access needs --enable-cors-header
description: Recent ComfyUI builds 403 cross-site browser requests; the CF Access redirect triggers it. Fix is --enable-cors-header https://comfyui.synai.ai in compose command override.
type: project
---

ComfyUI's `create_origin_only_middleware()` (in `/app/server.py`) returns **HTTP 403 when `Sec-Fetch-Site: cross-site`** is present on the request. Browsers set this header on the navigation that follows a Cloudflare Access login redirect (origin = `home-server-mello.cloudflareaccess.com`, target = `comfyui.synai.ai` → cross-site).

**Why:** ComfyUI added CSRF/DNS-rebinding protection. By default it picks `create_origin_only_middleware`. Passing `--enable-cors-header <ORIGIN>` switches to `create_cors_middleware`, which skips the Sec-Fetch-Site check and emits proper `Access-Control-Allow-*` headers.

**How to apply:** In `/home/mello/docker-compose.yml`, the `comfyui:` service needs an explicit `command:` override (the Dockerfile CMD doesn't include the flag):
```yaml
command: ["python", "main.py", "--listen", "0.0.0.0", "--port", "8188", "--enable-cors-header", "https://comfyui.synai.ai"]
```
Then `docker stop comfyui && docker rm comfyui && docker compose up -d comfyui`. (Plain `docker restart` does NOT re-read compose.)

**Symptom signature** (so future-you recognizes it fast): comfyui.synai.ai shows a 403 page *after* the CF Access login completes, even though the auth log shows `allowed: true` for the user. The 403 is the **origin** rejecting the post-login navigation, not Cloudflare Access. Quick test from the host: `curl -H 'Host: comfyui.synai.ai' -H 'Sec-Fetch-Site: cross-site' http://localhost:8188/` — if that returns 403, the flag is missing.

**Internal callers are not affected** because container-to-container HTTP doesn't send Sec-Fetch-Site (it's a browser-only Fetch Metadata header). So `claude-telegram` ("Joe"), `dreamvault-gen`, etc., calling `http://comfyui:8188` keep working with or without this flag — this fix is purely about browser access through the public domain.
