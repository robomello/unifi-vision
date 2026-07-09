---
name: matomo-analytics
description: Matomo 5 self-hosted analytics -- 11 tracked sites, CF Worker injection, daily Telegram report
type: project
---

Matomo 5 deployed 2026-04-03 for full website analytics across all Roberto's sites.

**Infrastructure:**
- Containers: `matomo` (port 8100) + `matomo-db` (MariaDB 11) on n8n-net
- Domain: matomo.synai.ai via CF Tunnel
- CF Worker `matomo-tracker` on `*.synai.ai/*` auto-injects tracking via HTMLRewriter
- GeoIP: DBIP-City-Lite installed, GeoIP2 provider enabled
- Archive: hourly systemd timer (`matomo-archive.timer`)
- Daily report: 8am Telegram via Joe (`matomo-report.timer`)

**Sites (11 total):**
| ID | Site | Tracking Method |
|----|------|----------------|
| 1-5, 7-9 | synai.ai subdomains | CF Worker injection |
| 6 | drinkwaretrove.com | Built into Next.js layout.js |
| 10 | evolutionlabs.blog | Built into site_builder.py |
| 11 | mellosdesigns.com | Built into React Router root.jsx |

**Why:** Roberto had zero user-facing analytics. Infrastructure monitoring (Prometheus) existed but nothing tracked page views, referrers, geography, or funnels.

**How to apply:** When adding new sites, register in Matomo API + either add to CF Worker SITE_MAP (synai.ai) or embed tracking script directly (external domains).
