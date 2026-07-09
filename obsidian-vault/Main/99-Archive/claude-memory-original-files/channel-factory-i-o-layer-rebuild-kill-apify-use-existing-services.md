---
name: Channel Factory I/O Layer Rebuild (kill Apify, use existing services)
description: Channel Factory pipeline I/O rewire: kill Apify/Facebook scraper, kill custom YouTubeChannelManager, replace with youtube-uploader:8055 + HUNTER_YOUTUBE_API_KEY from ~/.env, keep LangGraph 7-stage pipeline untouched
type: project
---

# Channel Factory — I/O Layer Rebuild Plan

LangGraph pipeline at `/home/mello/channel-factory/` is architecturally sound (7-stage pipeline, Claude CLI, ComfyUI QwenVL vision, state validation). I/O layer was built with **wrong dependencies** (Apify, custom YouTube OAuth) instead of existing infrastructure (youtube-uploader:8055, env vars from `~/.env`). Rewire I/O without touching pipeline logic.

## Keep Untouched (architecturally sound)

- LangGraph: `agents/graph.py` orchestration, state machine, conditional edges
- All 7 agent nodes: ingest, analyze, research, blueprint, build_pipeline, setup, first_batch
- `utils/claude_client.py` — Claude CLI + ComfyUI QwenVL vision (correctly implemented)
- `agents/state.py` — Pydantic validation, state typing, prompt sanitization
- `server.py` — FastAPI, rate limiting, auth, timeouts, image handling
- `main.py` — CLI interface

## What's Broken (to rip)

1. **Apify** — `utils/scraper.py` `FacebookScraper` imports `apify_client`. Roberto has no Apify account.
2. **Custom `YouTubeChannelManager`** — `utils/youtube_client.py:147-297` reinvents OAuth flow that **`youtube-uploader:8055`** already handles
3. **`config.yaml` for API keys** — should come from env vars (`~/.env`), not a checked-in YAML
4. **`requirements.txt`** lists `apify-client`, `google-auth-oauthlib`, `google-auth-httplib2` (remove)
5. **n8n workflow template** contains Apify/Facebook scraping nodes (will never work)

## Comprehensive YouTube URL Regex (replaces FacebookScraper)

In `ContentParser.extract_youtube_url(text)`:

```python
_YT_URL_RE = re.compile(
    r'https?://(?:www\.|m\.)?'
    r'(?:'
    r'youtube\.com/(?:watch\?v=[\w-]+|shorts/[\w-]+|embed/[\w-]+|'
    r'channel/[\w-]+|c/[\w-]+|@[\w.-]+|user/[\w-]+|playlist\?list=[\w-]+)'
    r'|youtu\.be/[\w-]+'
    r')'
)

@staticmethod
def extract_youtube_url(text: str) -> list[dict]:
    """Returns [{url, type}] where type ∈ {video, channel, short, playlist}."""
```

Classification rules:
- `/channel/`, `/c/`, `/@`, `/user/` → `channel`
- `/shorts/` → `short`
- `/playlist` → `playlist`
- else → `video`

## ingest.py Rewire

- Remove `FacebookScraper` import. Use `ContentParser` only.
- Function signature: remove `fb_scraper` param, add **optional** `yt_research: Optional[YouTubeResearchClient]`
- URL handling:
  - YouTube channel URL → `yt_research.search_channels()` + `get_channel_videos()` → store as scraped content
  - YouTube video/short URL → extract video ID → `yt_research.get_video_stats()` for details
  - Facebook or other → log warning, skip scraping, **graceful degradation** (tell user to provide text)
- If `yt_research is None` (missing API key) → log warning, fall through to **text-only mode**. DO NOT crash.
- Wrap `yt_research` calls in try/except with same fall-through behavior.

## YouTubeResearchClient — None-Safe

`utils/youtube_client.py`:
```python
def __init__(self, api_key: str = None):
    key = api_key or os.environ.get("HUNTER_YOUTUBE_API_KEY", "")
    if not key:
        self.client = None
        return  # None-safe; caller checks
    ...
```

Remove (only needed by deleted YouTubeChannelManager):
- `google_auth_oauthlib.flow.InstalledAppFlow`
- `google.auth.transport.requests.Request`
- `google.oauth2.credentials.Credentials`
- `SCOPES_READ`, `SCOPES_WRITE` constants

## youtube-uploader:8055 Replaces YouTubeChannelManager

The Mello server already runs a `youtube-uploader` service on port 8055 that handles the OAuth flow + uploads. Channel Factory just POSTs to it instead of reinventing the wheel.

## Env Vars (from `~/.env`)

- `HUNTER_YOUTUBE_API_KEY` — YouTube Data API v3 key for `YouTubeResearchClient`
- Plus any uploader service URL/token already in `.env`

Delete `config.yaml`. No more API keys checked in.

## Verification

- `agents/graph.py` smoke test runs end-to-end on a YouTube channel URL with `HUNTER_YOUTUBE_API_KEY` unset → completes in text-only mode with WARNING logs, no crash
- Same with API key set → actual channel/video metadata appears in scraped content
- Facebook URL → warning logged, pipeline proceeds with user-provided text
- `pip install -r requirements.txt` no longer pulls `apify-client` etc.
