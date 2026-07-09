---
name: Global Gas App
description: Global fuel price PWA at gas.synai.ai -- architecture, data sources, decisions, and roadmap
type: project
---

## Overview
Global fuel price comparison app inspired by PhillyGasAlerts.com but worldwide. Live at https://gas.synai.ai.
**Tagline**: "See the savings." Heatmap is the key differentiator.

## Architecture
- **Frontend**: React 19 + Vite 8 + Tailwind v4 + Leaflet + motion (framer-motion v12)
- **Backend**: Express 5 + SQLite (Drizzle ORM) + node-cron
- **Deployment**: Docker on port 3025, Cloudflare tunnel, n8n-net network
- **Location**: `/home/mello/commander/projects/global-gas/`
- **Spec**: `gas-app-spec.md` in project root (comprehensive product spec from Claude Desktop)

## Data Sources (as of 2026-04-02)
| Source | Country | Stations | Cost | Schedule |
|--------|---------|----------|------|----------|
| Prix Carburants | France | ~10K | FREE | 15 min cron |
| MITECO | Spain | ~12K | FREE | 6h cron |
| E-Control | Austria | ~400 | FREE | 15 min cron |
| Tankerkoenig | Germany | ~4K | FREE (demo key) | 30 min cron |
| Google Places | US | ~1K+ | PAID ($40/1K) | On-demand only, max 1/day/zone |
| Pure-Gas.org | US | ~17.6K | FREE | Weekly (ethanol-free locations) |
| World Bank | 111 countries | averages | FREE | Weekly CSV |

**Total**: ~45,000 stations

## Key Decisions (2026-03-30 to 2026-04-02)
- **No ads ever** -- pure freemium model (free + Pro at $3-5/mo)
- **iOS**: Native Swift (not Capacitor/PWA wrapper) -- future phase
- **Google API cost control**: On-demand only, max 1 fetch per zone per 24 hours
- **Zone caching**: Geohash precision 4 (~39km cells), demand-driven, zones deactivate after 48h inactivity
- **Heatmap always on Regular 87** regardless of selected fuel filters
- **Multi-fuel select**: Users can toggle multiple fuel types simultaneously
- **Ethanol-free**: Green "EF" markers from pure-gas.org, octane info in popups

## Tankerkoenig (Germany)
- Demo key `00000000-...0002` returns fake data -- registered for real key on 2026-04-02
- Registration at onboarding.tankerkoenig.de, email: mello_roberto@hotmail.com, company: The Mellos Designs LLC
- Manual review required, may take days
- Once approved: switch to daily dump (all 14K stations) instead of city-by-city queries
- Attribution required: CC BY 4.0, link to tankerkoenig.de

## Brazil
- Google Places returns stations but NO fuel prices for Brazil
- ANP (gov) data portal is broken/inaccessible via API as of 2026-04-02
- World Bank has country-level averages (~$1.30/L gasoline)
- Station-level Brazil prices would need scraping of local sites

## PWA Features (built 2026-03-30)
- Installable from browser (vite-plugin-pwa + Workbox)
- CartoDB dark map tiles (native dark, no CSS inversion)
- Glass morphism UI (glass-panel, glass-surface utilities)
- Mobile: BottomNav (Map/Search/Favorites/Settings) + BottomSheet (peek/half/full)
- Desktop: Glass sidebar + full header with fuel chips
- Spring animations via motion/react library
- Service worker caches stations (NetworkFirst), stats (StaleWhileRevalidate), tiles (CacheFirst)

## Spec Roadmap (from gas-app-spec.md)
- Phase 1: Backend refactor + caching -- DONE (zone system, smart refresh)
- Phase 2: Free data source integration -- PARTIAL (DE added, UK/AU/EIA pending API keys)
- Phase 3: API layer + auth (JWT, Sign in with Apple) -- NOT STARTED
- Phase 4: Web app enhancement (EV layer, trends, currency switching) -- NOT STARTED
- Phase 5: iOS native app (Swift + MapKit) -- NOT STARTED
- Phase 6: Pro features (commute mode, fill-up tracker, widgets) -- NOT STARTED
- Phase 7: Launch (TestFlight, App Store) -- NOT STARTED
