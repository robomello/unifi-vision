---
name: Env Files & Credential Layout
description: Where all .env files and API credentials live on mello-server, how to find them fast, and the current Google OAuth client situation — stop hunting, run find first
type: reference
originSessionId: google-workspace-cli-session
---
# Env Files & Credential Layout

**Rule: to find any credential, run `find` FIRST — do not guess paths or "look around".**

```bash
# every .env on the box (73 of them):
find /home -type f \( -name '.env' -o -name '.env.*' -o -name '*.env' \) -not -path '*/node_modules/*'
# only the ones holding real creds:
grep -rlE 'GOCSPX-|GOOGLE_CLIENT_(ID|SECRET)|GOOGLE_REFRESH_TOKEN|_TOKEN|_SECRET|_KEY' $(find /home -name '.env' ...)
```

## Primary secrets file
`/home/mello/.env` — the master env (~23 KB). Holds Google, YouTube (per-channel refresh tokens), Etsy, LinkedIn, Nest, Gemini, RunPod, Admin, etc. **This is the first place to look for any API key.** When someone says "the creds you already use," they mean this file (loaded into agent/tool runtime), NOT the top-level shell env — `env | grep GOOGLE` is empty because they are injected at tool/agent spawn, not exported to interactive shells.

## Other cred-bearing env files
- `/home/mello/commander/projects/dream/web/.env`
- `/home/mello/commander/projects/pawtraits/.env`
(Only these 3 of the 73 contain Google creds.)

## Google OAuth clients (project `commander-480320`, project number `602087126576`)
Two DIFFERENT OAuth clients share the project number:
- **`602087126576-f38…`** — the Workspace client used by `commander/tools/google_docs.py` (scopes: documents + drive). Referenced by `GOOGLE_CLIENT_ID`/`GOOGLE_CLIENT_SECRET`/`GOOGLE_REFRESH_TOKEN` in `/home/mello/.env`. **As of this session its secret in `.env` is STALE** → Google returns `invalid_client: The provided client secret is invalid` (client is recognized, secret was rotated). Fix = copy current secret from Cloud Console → project commander-480320 → Credentials → the `-f38…` client → update line 20 of `/home/mello/.env`.
- **`602087126576-n7e…`** — the "web" client in `client_secrets.json` (secret `GOCSPX-32j…`, redirect `http://localhost:8055/auth/callback`). Different client; the `.env` refresh token is NOT bound to it (returns 400).

`client_secrets.json` copies live at: `/home/mello/client_secrets.json`, `/home/mello/commander/projects/youtube-uploader/client_secrets.json`, `/home/mello/youtube-uploader/client_secrets.json` (all identical, all the `-n7e…` web client).

## What actually authenticates on disk right now
Exhaustive test (5 client_ids × 5 secrets × 13 refresh tokens across all 3 env files): exactly ONE working refresh — the **Nest / Smart Device Management** cred (`client_id 151952771234…`, scope `https://www.googleapis.com/auth/sdm.service`). No Workspace (docs/drive) triple on disk currently refreshes.

## google-workspace-cli (gws)
gws is a standalone CLI; it reads creds from `GOOGLE_WORKSPACE_CLI_TOKEN` or `GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE`, which runtime injection does NOT populate. To test gws: fix the `-f38…` secret in `.env`, then feed gws that working triple (or use a service account for unattended/headless).
