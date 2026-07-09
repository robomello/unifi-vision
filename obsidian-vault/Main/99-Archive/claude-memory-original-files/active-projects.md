---
name: Active Projects
description: Current projects with status and next steps
type: project
originSessionId: <REDACTED-UUID-1>
---
## Dream - AI Image Generation Webapp
- **Status**: Deployed and running (dream-web + dream-worker containers healthy as of 2026-04-08)
- **Location**: `/home/mello/commander/projects/dream/`
- **What's next**:
  1. Create real Stripe Products/Prices + webhook endpoint
  2. Phase 2: Cloud model cost research + MyDesigns integration

## Dara LoRA
- **Status**: Dormant since 2026-03-25 (collecting reference images)
- **Next**: Install 2 custom nodes, update workflow JSON, test

## Channel Factory
- **Location**: `/home/mello/channel-factory/`
- **Status**: Running (`channel-factory` + `factory-agent` containers active)

## Decay Pipeline (Osteology Content)
- **Location**: `/home/mello/commander/projects/decay_pipeline/`
- **Status**: Running (`decay-viewer` container active)

## Luxurious Cabins (home-tour video pipeline)
- **Location**: `/home/mello/commander/projects/luxurious-cabins/`
- **Domains**: `luxurious-cabins.synai.ai` (primary) + `home-tours.synai.ai` (alias), both Google-OAuth gated
- **Status**: Renamed from `home-tour-gen` on 2026-04-22. Dockerized FastAPI on port 8071, 8-stage async orchestrator, 7/8 stages verified working.
- **Engines**: images (qwen2512, flux2, nano-banana); videos (hunyuan15, kandinsky5, ltx2-dev, ltx2-distilled, wan22, wan22-lightspeed); tts (fish); qa (qwenvl); db (nocodb); audio (foley); assembly
- **Blocker**: needs ComfyUI API-format workflow JSONs captured for video engines + TTS + Foley
- **See**: [Luxurious Cabins](luxurious-cabins.md)

## LTX-2 Reference-to-Video
- **Status**: Dormant since 2026-03-25 (research complete, test pending)

## Conectitude (Gisele's Parenting Channel)
- **Location**: `/home/mello/commander/projects/conectitude/` (13 modules)
- **Status**: Code complete (2026-03-26), not yet integration tested
- **Blocking**: Gisele voice sample (for F5-TTS cloning; using Kokoro fallback)
- **Next**: Run full pipeline on a Parentitude video, review quality, fix issues

## FB Monitor (Facebook Image Downloader)
- **Location**: `/home/mello/commander/projects/fb-monitor/`
- **Status**: Deployed and running (2026-03-29). Container `fb-monitor`, bot `@fb_extract_bot`
- **What it does**: Monitors Facebook profiles, auto-downloads new images via gallery-dl every 10 min
- **Seeded**: Rizan Dadoush (389 images)

## Piracy Monitor (Claude Code IP Protection)
- **Location**: `/home/mello/commander/tools/piracy_monitor/`
- **Status**: Built and tested (2026-03-31). Cron DISABLED -- community already reporting.
- **What it does**: Scans GitHub for Claude Code piracy repos, scores 0-100, Telegram alerts + auto-files issues on anthropics/claude-code
- **Next**: Re-enable cron if community reporting dies down

## Global Gas (gas.synai.ai)
- **Location**: `/home/mello/commander/projects/global-gas/`
- **Status**: Live PWA with 45K+ stations (2026-04-02). Backend zone caching done. Tankerkoenig key pending.
- **Stack**: React + Vite + Tailwind + Leaflet + Express + SQLite + Docker
- **What's next**: 
  1. Activate Tankerkoenig with real API key (waiting on approval email)
  2. Phase 3: API auth layer (JWT, Sign in with Apple)
  3. Phase 5: iOS native app (Swift + MapKit)
- **Spec**: `gas-app-spec.md` in project root
- **Key decisions**: No ads ever, pure freemium, native Swift for iOS, Google on-demand max 1/day/zone

## FORGE (Agent Orchestration Platform)
- **Location**: `/home/mello/forge/`
- **Status**: Mature backend, UI polish complete (2026-04-03 "Kinetic Command" upgrade). Auth via CF Access (Google OAuth + email OTP).
- **Port**: 3201 (no subdomain yet)
- **Blocking**: 3 HIGH security issues (JWT bypass, SQL injection pattern, unvalidated cron) -- must fix before wider exposure
- **What's next**:
  1. Fix HIGH security issues from SECURITY_REVIEW.md
  2. Add Cloudflare Tunnel route (forge.synai.ai)
  3. Remaining 4 UI polish items
  4. Test suite (zero tests currently)

## SafePlate (Restaurant Allergen Safety)
- **Location**: `/home/mello/commander/projects/safeplate/`
- **Status**: Deployed and running healthy (container `safeplate` up since 2026-04-05). i18n for 7 languages.
- **Stack**: Next.js 15 + Prisma 6 + PostgreSQL + Tailwind + Leaflet
- **Port**: 3030, subdomain: safeplate.synai.ai
- **What's next**: Add CF Tunnel route for safeplate.synai.ai, seed restaurant data

## Pawtraits (AI Dog Portraits)
- **Location**: `/home/mello/commander/projects/pawtraits/`
- **Status**: Live at pawtraits.synai.ai (port 3101). CF edge caching configured.
- **Recent**: Flashlight effect reworked (images always visible), CF caching optimized (2026-04-04)

## CodeForge Arena (LLM Benchmarking)
- **Location**: `/home/mello/commander/projects/codeforge-arena/`
- **Status**: Live at arena.synai.ai (port 9099). 3 benchmark types: Full-Stack, Coding, Agent.
- **Recent**: Nemotron Cascade 2 added (2026-04-05), Agent Bench integrated (2026-04-06), VP presentation delivered (2026-04-07)
- **Next**: Continue running agent benchmarks, iterate on dashboard based on VP feedback

## Social Posting Pipeline
- **Location**: `/home/mello/commander/projects/social_posting/`
- **Status**: Multi-session planning + implementation (2026-04-05 to 2026-04-06). Builds LinkedIn/social media posting system from weekly JSON content packs.
- **What it does**: Reads content-pack JSON files (themes, copy, image prompts, video scripts), posts to LinkedIn/FB/X/Instagram/TikTok/YouTube on schedule
- **Container**: `social-posting` (confirmed running 2026-04-07)

## Mercedes Inspection Vision
- **Status**: Running (container `gspoc-inspect` up 10 days as of 2026-04-08)
- **GPU**: MUST use GPU 1 (RTX PRO 6000 Blackwell 96GB)

## Etsy Competitor Tracker
- **Status**: Built (2026-04-05). Agent created for Etsy competitor price monitoring.
- **Agent**: `etsy-competitor-tracker` -- nightly price scrapes, price change alerts, listing tracking, price history
- **Context**: Part of "intelligent sales" strategy to optimize pricing based on competitor behavior

## Obsidian (Note-Taking)
- **Container**: `obsidian` (linuxserver/obsidian), port 8099
- **Status**: Running. Internal only (no CF Tunnel). Black screen issue reported 2026-04-07.
