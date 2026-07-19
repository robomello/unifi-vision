# Home Infrastructure — What's Actually Running

**Last updated:** 2026-07-19
**Source:** Home server `docker ps` output + Claude Code memory

> [!note] Claude Code tooling (added 2026-07-19)
> Two developer-tooling additions on the home server — see [[2026-07-19]]:
> - **RTK ("Rust Token Killer")** `v0.42.4` at `/home/mello/.local/bin/rtk` — token-optimizing CLI proxy wired in as a Claude Code PreToolUse hook (`rtk hook claude`). Repo: `/home/mello/repos/headroom/`. Claims 60–90% token savings on dev ops.
> - **`cleanup-dead-sessions` skill** at `~/.claude/skills/cleanup-dead-sessions/` — safely reaps dead/orphaned Claude swarm tmux sessions + stale `claude-swarm-*` sockets. Relevant to the disk-at-80% concern below.

## Running services (75+ containers, 4 hours uptime as of 2026-04-19 19:00 CST)

### Core infrastructure
- **cloudflared** — Cloudflare tunnel (exposes synai.ai subdomains)
- **nginx** via claudicle-ui, etc. — reverse proxies
- **promtail, loki, prometheus** — observability stack
- **cadvisor** — container metrics
- **server-health-monitor** — healthy ✓

### Databases & message brokers
- **n8n-postgres** — PostgreSQL (with pgvector extension for vector memory)
- **n8n-redis** — Redis (queue backend, caching)
- **surrealdb + surrealist** — graph DB + UI
- **nocodb** — structured data/tables at port 8090
- **matomo + matomo-db** — web analytics for 11 sites
- **claudicle-clickhouse** — Claude Code telemetry DB

### Commander + its helpers
- **commander** — central agent hub (port 8070, `cmd.synai.ai`) — *healthy*
- **mcp-server** — MCP endpoint (`mcp.synai.ai`)
- **memory-mcp** — semantic memory server (pgvector backend)

### n8n cluster
- **n8n-main** + **n8n-worker-1/2/3** — workflow orchestration
- **n8n-db-cleaner** — periodic cleanup

### Telegram bots
- **garden-telegram** — mello-garden bot
- **claude-telegram** — Joe/Claude bot, GLM5 approval hook (*healthy*)
- **pipeline-telegram** — pipeline triggers
- **image-telegram** — image gen bot (*healthy*, 3hr uptime)
- **etsy-telegram** — Etsy listing ops
- **street-camera-bot** — street camera monitoring
- **fb-monitor** — `@fb_extract_bot`, Facebook image auto-download

### Content production pipelines
- **channel-factory** + **channels-runner** — YouTube channel factory (channels-runner **restarting** — known issue)
- **factory-agent** — FastAPI pipeline agent (*healthy*)
- **videogen-factory** (*healthy*) + **videogen-worker** — video generation
- **deep-origins** — evolution lineage pipeline (port 8060)
- **youtube-uploader** + **youtube-hunter** (*healthy*) — YouTube operations
- **decay-viewer** — osteology content pipeline
- **yt-analyses** — YouTube analytics
- **dreamvault-gen** — image gen bot
- **avatar-pipeline** (*healthy*) — avatar generation
- **dream-web** (*healthy*) + **dream-worker** (*healthy*) — Dream AI webapp

### Web products live (synai.ai subdomains)
- **safeplate** (*healthy*) — restaurant allergen safety, port 3030
- **pawtraits-web** (*healthy*) + **pawtraits-worker** (*healthy*) — AI dog portraits, port 3101
- **mellobooks-web** + **mellobooks-api** — MelloBooks (memory says "dead" but containers running — worth verifying)
- **great-3d-impressions** (*healthy*) — Great3DImpressions Shopify storefront
- **drinkwaretrove-gallery** (*healthy*) — DrinkwareTrove gallery
- **casa-web** + **casa-api** — Casa AI (memory says "dead" but containers running — worth verifying)
- **global-gas** — gas.synai.ai, 45K station PWA
- **roi-static** — roi.synai.ai dashboard
- **privacy-policy** — privacy policy pages

### AI / ML / Compute
- **ollama** — local LLM inference
- **ollama-embed** — embeddings
- **comfyui** — image/video generation (MUST use GPU 1 = RTX PRO 6000 Blackwell)
- **comfyui-proxy** — ComfyUI reverse proxy
- **whisper-stt** (*healthy*) — speech-to-text
- **viqa** — **[[OTTO|VIQA]] container is running on home server** — worth checking what state it's in

### Specialty bots & services
- **sonos-player** — Sonos control
- **printwalk** — PrintWalk integration
- **obsidian** — Obsidian GUI container (port 8099, internal only)
- **forge** (*healthy*) — agent orchestration platform
- **ai-psychologist** (*healthy*) — Dr. Sofia app for [[Gisele]]
- **safeplate** (*healthy*) — allergen safety
- **mello-garden** (*healthy*) — garden monitoring
- **skool-api** (*healthy*) — Skool community API
- **social-posting** — LinkedIn/FB/X posting pipeline
- **linkedin-gems** — LinkedIn content
- **gasbuddy-scraper** — gas price scraping
- **flaresolverr** — Cloudflare challenge solver

### Telemetry
- **claudicle-ui** + **claudicle-otel** + **claudicle-clickhouse** — Claude Code usage dashboard (`claudicle.synai.ai`)

## Disk state

- **361 GB free of 1.8 TB (80% used)** — worth monitoring, not yet critical
- Both `/data` and `/home/mello` on the same device

## GPU state

- **NVIDIA RTX PRO 6000 Blackwell Max-Q Workstation Edition**
- 97,887 MiB total, 2,145 MiB used, 0% utilization at 31°C (cool and idle)

## Memory

- 65 GB total, 39 GB available — healthy

## What this reveals

Roberto runs **a substantial production infrastructure**. This is not a hobbyist setup. It's closer to a small managed-services business running a lot of live endpoints, many of which are healthy and under continuous use ([[Gisele]]'s AI psychologist, multiple Telegram bots people use, public webapps at safeplate/pawtraits/global-gas/forge, etc.).

**Strategic observation:**
The "dead projects" list in preferences (Casa AI, MelloBooks, Companion, etc.) is partially inconsistent with running containers. Either:
- The containers are orphans that should be cleaned up (disk at 80%)
- The projects aren't as dead as described

Either answer is actionable.

## Issues to flag

1. **`channels-runner` restarting** — known crash-loop, not yet investigated
2. **Disk at 80%** — 361 GB free but trajectory matters. Monitor.
3. **`mellobooks-web` and `mellobooks-api` running** — Roberto says "MelloBooks is dead." Either clean up or re-evaluate status.
4. **`casa-web` and `casa-api` running** — same question for Casa AI.
5. **`viqa` container running on home server** — what's the relationship to the OTTO-server [[OTTO|VIQA]]/[[OTTO|CNN Inspection]]? Worth verifying.

## See also

- [[Commander]] — the orchestration hub for most of this
- [[Claude-Code-Memory-Index]] — the 65+ memory files documenting individual projects
- [[Etsy-Shops]] — the idle 3D print farm piece of this infrastructure
- [[Gisele]] — AI Psychologist and Conectitude live here
