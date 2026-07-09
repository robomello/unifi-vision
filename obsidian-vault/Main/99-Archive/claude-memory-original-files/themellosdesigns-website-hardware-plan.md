---
name: TheMellosDesigns Website + Hardware Plan
description: mellosdesigns.com (Vercel SSG, React Router v7, Stripe, 3D-printed skeleton parts) + mellos-hardware (FastAPI on port 8078, mellos.synai.ai, Etsy sales auto-sync)
type: project
---

## TheMellosDesigns Website + Hardware Plan

### mellosdesigns.com (E-commerce Website)

**Path:** /home/mello/theMellosDesigns/
**Deployment:** Vercel (NOT Docker)
**Status:** Active, deployed at mellosdesigns.com
**Stack:** React Router v7, SSG (ssr: false + prerender), Vite 7.3, Stripe SDK, Framer Motion, Vercel Analytics + Speed Insights

**What it does:** Public-facing e-commerce website for TheMellosDesigns Etsy shop. Sells 3D-printed Halloween skeleton reinforcement parts (12ft Skelly, Jack Skellington, Predator, Inferno, Werewolf). Pre-rendered product pages with 6 categories.

**Key files:**
- react-router.config.ts — SSG prerender config, reads src/products.json, slug generation
- vercel.json — build command, SPA fallback rewrites
- GEO_AUDIT_2026-03-15.md — GEO audit scoring 86/100
- scripts/generate-sitemap.js — auto-generated sitemap on build

**GEO optimization applied:** JSON-LD stacking (Product + HowTo + FAQPage + BreadcrumbList), FAQ content, comparison tables, real Etsy reviews. Matomo tracked as site #11.

### mellos-hardware (Hardware Purchase Plan)

**Path:** /home/mello/commander/projects/mellos-designs/hardware-page/
**Container:** mellos-hardware (running, healthy)
**Port:** 127.0.0.1:8078 (tunnel: mellos.synai.ai, CF Access protected)
**Stack:** FastAPI + single-page HTML, dark theme, mobile-responsive with odometer wheel pickers

**What it does:** Internal editable purchase-plan web app. Tracks screw/insert consumption per product, YTD sales, inventory counts, calculates what to buy. Two tabs: Hardware (screws/inserts) and Products & Filament. Auto-syncs with Etsy sales via etsy-telegram bot every 5 minutes.

**Key files:**
- app.py — FastAPI (295 lines), endpoints: /api/plan (GET/POST), /api/sales-sync (POST from etsy-telegram)
- index.html — Single-page app (691 lines), dark theme, mobile-responsive
- data/plan.json — Persistent data, last updated 2026-06-11
- screws-bom.md — Per-product screw BOM, 30 products

**Gotchas:**
- LISTING_MAP maps 29 Etsy listing IDs to 30 products (product #30 Predator Ankle has no active listing)
- PRODUCT_BOM maps products to hardware rows; sales-sync recomputes YTD/needed without touching manual fields
- Sales declined 2024->2025: 829 orders/1210 items/48.7k down to 645 orders/908 items/40.3k
- 2026 plan based on 0% growth (flat vs 2025)

Why: mellosdesigns was a MISSING SOURCE in the consolidated memory. Both the public website and internal hardware planner are active production services.

How to apply: When working on mellosdesigns.com, remember it is Vercel-hosted (not Docker). For hardware plan, use the mellos-hardware container on port 8078 via mellos.synai.ai.
