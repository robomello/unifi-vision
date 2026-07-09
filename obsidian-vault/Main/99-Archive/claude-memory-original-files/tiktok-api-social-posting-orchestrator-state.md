---
name: TikTok API + social_posting orchestrator state
description: Roberto has TikTok Content Posting API approved (creds in .env.postiz, redirect at postiz.synai.ai). His social_posting service has fb/ig/li/x posters but NO TikTok poster yet. No OAuth done for @robomello79.
type: reference
---

**TikTok API access**

- Roberto has the **Content Posting API** approved at developers.tiktok.com.
- Credentials live in `/home/mello/social-auto-stack/.env.postiz` as `TIKTOK_CLIENT_KEY` and `TIKTOK_CLIENT_SECRET`.
- Registered redirect URI is `https://postiz.synai.ai/...` (confusingly named — Postiz was the original integration target but is no longer used; the redirect domain still matches because the app registration was filed pointing at that hostname).
- TikTok Shop **Affiliate Open Platform** (Path 2 — sample-request / commission API) is NOT registered. Requires a separate dev portal application at partner.tiktokshop.com.

**social_posting service**

- Container name: `social-posting` (NOT Postiz despite the env filename — it's Roberto's own custom FastAPI/APScheduler service).
- Source: `/home/mello/commander/projects/social_posting/social_posting/`.
- NocoDB-backed scheduler reads from table id `moapl0l57rfvdxv` with states `POSTING / READY / PENDING_APPROVAL / APPROVED / MISSED`.
- Network: `n8n-net`, no host port binding (internal only on container port 3000).
- Watches `/app/packs` for new content-pack JSON files (one per day, multi-platform).
- Posters are at `social_posting/posters/`: linkedin.py, x.py, facebook_image.py, instagram_image.py.
- **TikTok poster does NOT exist yet** — must be built. Pattern mirror: take a content pack platform block, upload MP4 + caption + hashtags via `/v2/post/publish/video/init/` and poll `/v2/post/publish/status/fetch/`.

**OAuth state**

- No access_token or refresh_token visible anywhere for `@robomello79`.
- Has to run the OAuth flow once: auth URL with scopes `user.info.basic,video.upload,video.publish`, callback exchange, store tokens.
- `social-posting` does not appear to have a `/oauth/tiktok/callback` route either — needs adding alongside the poster module, or a one-shot CLI OAuth helper that the user runs manually.

**For the TikTok Shop project (`@robomello79`)**

- Until the TikTok poster is built and OAuth completed, `tiktok-shop-agent.upload_video` runs through browser-agent + cookies (`mello/.cookies/tiktok-robomello79.json`).
- After build: `tiktok-shop-agent.upload_video` writes a content pack to `social-posting`'s NocoDB table; the orchestrator handles auth, upload, polling, status reporting.

**Path 2 future work**

- Register Affiliate Open Platform app at partner.tiktokshop.com under one of Roberto's business entities (Drinkware Trove default candidate).
- Adds: programmatic sample requests, commission pulls, conversion attribution via webhooks.
- 5-10 day approval gate.
