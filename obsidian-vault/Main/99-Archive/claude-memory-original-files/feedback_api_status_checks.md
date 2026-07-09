---
name: Test the specific operation, not a proxy
description: When asked "is X working?", test the exact path the user will use -- not a convenient nearby read endpoint
type: feedback
originSessionId: <REDACTED-UUID-14>
---
Before reporting a service/API as "working," test the specific operation the user is about to perform (downloads, writes, auth-gated endpoints) -- not a convenient nearby read endpoint.

**Why:** On 2026-04-16, Roberto asked "is the Civitai API working?" immediately after discussing a LoRA download. I ran GET on `/api/v1/models` and `/api/v1/creators`, got 200 OK on both, and answered "yes, up." Those endpoints almost never fail. His actual intent was a download, which went through `/api/download/models/...` -- auth-gated and 401 for anonymous callers. My "working" answer delayed the real next step (getting a Civitai API token).

**How to apply:**
1. Infer intent from surrounding context. What is the user about to do with this service? Test THAT path.
2. If the user is about to download, HEAD the download URL. If they're about to write/POST, test the write. If auth is involved, verify the auth path.
3. If you can only test a narrow slice, say so explicitly: "Public read endpoints respond, but I haven't verified [the thing you need]."
4. Never generalize from happy-path reads to "the API works."
5. When in doubt, ask "what operation are you planning?" before reporting status.
