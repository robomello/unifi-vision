---
name: Mellos Designs hardware plan page (mellos.synai.ai)
description: Editable screw/insert purchase plan page at mellos.synai.ai; BOM + plan docs in commander/projects/mellos-designs
type: project
---

Editable hardware purchase-plan page for TheMellosDesigns Etsy shop, built 2026-06-10.

- URL: https://mellos.synai.ai (Cloudflare Access protected; allowed: mello_roberto@hotmail.com, robomello79@gmail.com only)
- Service: mellos-hardware container (FastAPI, port 8078, n8n-net), code at ~/commander/projects/mellos-designs/hardware-page/, data persists in hardware-page/data/plan.json
- Responsive: desktop = dense table; phones (<=740px) = card layout; mobile number entry via custom iOS-style odometer wheel picker (endless drums, carry/borrow, tick sound, clamps 0-9999)
- Static analysis docs: ~/commander/projects/mellos-designs/screws-bom.md (per-product screw BOM, 30 products) and purchase-plan-2026.md (2024/2025/2026 usage + needed; flat 0% growth basis since sales declined 2024->2025: 1210 -> 908 items)
- 12 screw SKUs + 5 heat-set insert SKUs; biggest mover: hex flat M6x35 (~2.4k/yr) and M6 inserts (~2.8k/yr); sales are Halloween-driven (Aug-Oct)
- Product #13 (Leaping Arches bases) screws still undefined, excluded from plan
- Etsy data pulled via tools/etsy_api.py EtsyClient(shop=2) get_receipts
