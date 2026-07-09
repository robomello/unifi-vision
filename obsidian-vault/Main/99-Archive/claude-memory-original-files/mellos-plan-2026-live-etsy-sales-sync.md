---
name: Mellos Plan 2026 live Etsy sales sync
description: mellos.synai.ai YTD numbers auto-sync from Etsy every 5 min via etsy-telegram bot -> POST /api/sales-sync
type: project
---

The Mellos Designs Plan 2026 page (mellos.synai.ai, container mellos-hardware) no longer holds static YTD sales: the etsy-telegram bot polls TheMellosDesigns (shop 2) receipts every 5 min (job `mellos_sales_sync`, handlers/sales_sync.py, first run 20s after bot start) and POSTs per-listing 2026 quantities to `http://mellos-hardware:8078/api/sales-sync`. That endpoint (hardware-page/app.py) maps listings to products via LISTING_MAP (29 listings -> products 1-29; #30 has no active listing), recomputes product ytd2026/needed and screw/insert consumption via PRODUCT_BOM (verified against screws-bom.md and 2025 totals), and persists plan.json — never touching manual fields (inventory/stock/notes/material) or plan["updated"]; sync timestamp lives in a separate `sales_synced` key.

Conventions: canceled receipts excluded (status compared case-insensitively — live API returns "Canceled"/"Fully Refunded" title-case despite docs claiming lowercase), fully-refunded receipts ARE counted (matches the original Jun-10 snapshot convention). Dedup state at /data/etsy-telegram/mellos_sales_state.json skips the POST when totals are unchanged. The page itself re-fetches every 5 min + on tab focus (refreshSales) and has collapsible product tiles (default collapsed, expanded set in localStorage `mellos-expanded-products`). plan.json backup from before the feature: hardware-page/data/plan.backup-2026-06-11.json. Related: [Mellos hardware purchase plan page](mellos-hardware-purchase-plan-page.md) if present.
