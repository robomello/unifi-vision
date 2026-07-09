---
name: Gmail Pipeline
description: End-to-end Gmail access (read, download attachments, draft, send) via OAuth — setup, token location, and tool paths
type: reference
originSessionId: <REDACTED-UUID-21>
---
# Gmail Pipeline

Two independent paths exist for Gmail, use whichever fits:

## Path A — claude.ai Gmail MCP (zero setup, read-only + draft)
Always available in sessions with the claude.ai Gmail connector. Tools: `gmail_search_messages`, `gmail_read_message`, `gmail_read_thread`, `gmail_list_labels`, `gmail_list_drafts`, `gmail_create_draft`, `gmail_get_profile`. Authenticated as `robomello79@gmail.com`.

**Gaps**: no attachment bytes, no label create/modify, no send.

## Path B — local Python tool (full read + send)
Script: `/home/mello/commander/tools/gmail_fetch_attachments.py`
Token:  `~/.credentials/gmail_token.json` (readonly + send scopes)
OAuth client: youtube-uploader GCP project `<REDACTED-GCP_PROJECT_NUM-1>`, client_secrets at `/home/mello/client_secrets.json` (symlink to `commander/projects/youtube-uploader/client_secrets.json`).

Redirect URI `http://localhost:8055/auth/callback` — registered in the GCP console, but since Roberto's browser is remote the callback server can't be reached. Workflow: script prints auth URL → Roberto opens, approves → copies the failing `localhost:8055/...` URL → script re-runs with `--auth-code "<url>"`.

### Common commands
```bash
# Fetch attachments by message ID
python3 gmail_fetch_attachments.py --message-id <id> --out /home/mello/Downloads/X

# Fetch by search
python3 gmail_fetch_attachments.py --search 'subject:"Claude check"'

# Draft (safe default)
python3 gmail_fetch_attachments.py --to foo@bar --subject S --body B

# Send (explicit)
python3 gmail_fetch_attachments.py --to foo@bar --subject S --body B --send

# Reply in thread
python3 gmail_fetch_attachments.py --thread-id <tid> --body "..." --send
```

## Gotchas
- Gmail API must be **enabled** in GCP project <REDACTED-GCP_PROJECT_NUM-1> (already done 2026-04-14).
- `client_secrets.json` redirect URIs can drift from Cloud Console — if `redirect_uri_mismatch` appears, add the URI in console (`https://console.cloud.google.com/apis/credentials?project=<REDACTED-GCP_PROJECT_NUM-1>`).
- `.edz` files are **7-zip archives**, not ZIP. Use `py7zr` (installed with `pip install --user --break-system-packages py7zr`).
- To add more scopes later: edit `SCOPES` in the script, `rm ~/.credentials/gmail_token.json`, re-run to re-consent.

## Addresses
- Primary Gmail: `robomello79@gmail.com`
- Roberto's hotmail (forward target for work emails): `mello_roberto@hotmail.com`
- Mercedes work: `roberto.mello@mercedes-benz.com`
