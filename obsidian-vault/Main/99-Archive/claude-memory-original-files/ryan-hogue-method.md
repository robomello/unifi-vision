---
name: Ryan Hogue POD Method
description: Ryan Hogue's data-driven Etsy POD workflow from his YouTube video, tools used, key principles, and combined design analysis approach
type: reference
---

## Source Video
- **Title**: "How I Find Winning Etsy Designs (Then Scale with AI)"
- **Channel**: Ryan Hogue Passive Income
- **URL**: https://youtu.be/mNSKDgc42QE
- **Published**: 2026-03-19
- **Duration**: 18:08
- **Full analysis**: `/home/mello/commander/projects/youtube-analyses/2026-03-19_ryan-hogue-passive-income_how-i-find-winning-etsy-designs-then-scale-with-ai.md`

## The 4-Step System
1. **Use ProfitTree to find what's already selling on Etsy** -- Chrome extension shows monthly sales, revenue, conversion rate, listing age under each Etsy listing. Web app has Product Finder with Niche Score, sortable data tables, and filters.
2. **Look for patterns -- don't copy designs** -- Identify winning phrases, humor styles, typography, design aesthetics, price points across top sellers.
3. **Use MyDesigns Dream AI to generate variations** -- Paste bestselling titles as prompts with a style suffix ("Vector illustration with thick outlines and bright flat colors. Isolated graphic on a transparent background and centered composition"). Nano Banana 2 model, 4:5 ratio (896x1120), 1K resolution, parallel prompts enabled.
4. **Publish at scale** -- BG remove > vectorize > Vision AI for SEO (auto titles/descriptions/13 tags) > canvas (Gildan 5000) > Printify mockups > bulk pricing > publish up to 120 listings at once.

## Key Principles
- **Start with demand, not design** -- work backwards from what customers already buy
- **Search BROAD niches** -- "taco" not "taco mug". Find cross-category demand signals.
- **Bestselling titles = AI prompts** -- the titles already describe what customers want
- **Filter for your model** -- Personalize: No, Listing Type: Physical (match what you actually sell)
- **File slot workflow** -- Main (raw AI) > Mockup 1 (bg removed) > Mockup 2 (vectorized SVG) > Mockup 3 (print-optimized)
- **Save publish config as profile** -- 2-click reuse on future batches

## Tools He Uses
- **ProfitTree** -- Etsy research (Chrome extension + web app). Discount code "RYAN" = 50% off.
- **MyDesigns** (mydesigns.io) -- AI generation, BG removal, vectorization, Vision AI SEO, canvas, mockups, publishing. Discount code "RYAN25" = 25% off.
- **Printify** -- Fulfillment via Printify Choice
- **Google Sheets + Notepad++** -- Data cleanup between ProfitTree export and prompt preparation

## Our Implementation
- **pod-research-agent** (`~/.claude/agents/pod-research-agent.md`) -- Built from this method, uses Alura + EverBee instead of ProfitTree for research
- **mydesigns-agent** -- Handles Dream AI generation, batch mode
- **Alura + EverBee cross-validation** replaces ProfitTree (Alura = opportunity score, EverBee = actual sales reality check)
- **Previous research output**: `/home/mello/commander/tools/pod_research_2026-03-22.md`
