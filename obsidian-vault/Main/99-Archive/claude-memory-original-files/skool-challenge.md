---
name: Skool AI Art Challenge
description: AI Art Sellers Collective monthly $1000 design challenge -- rules, judging criteria, prompt data in NocoDB, competitor shops
type: project
---

## The Challenge
- **Group**: AI Art Sellers Collective on Skool.com (run by Alec)
- **Prize**: $1,000/month split across 10 winners ($100 each)
- **Submit**: AI art image + the prompt used, via chat to Alec
- **Deadline**: End of month (e.g., March 31 midnight Central)
- **No limit** on submissions per person mentioned

## Judging Criteria
1. **Creativity** -- fresh, imaginative, emotionally powerful
2. **Composition** -- framing, balance, visual appeal
3. **Prompt Design** -- well-structured, original, effective
4. **Overall Impact** -- scroll-stopping, Etsy/Pinterest worthy

## NocoDB Data
- **Skool Posts table**: `m12djnm2een86w6` (223 posts, 36 from AI Art Sellers Collective)
- **Skool Prompts table**: `m3082prazskg7qd` (444 art prompts with generators)
- Generators: Midjourney (most), Dalle-3, Ideogram, Kittl
- Scraped via reverse-engineered Skool API at `/home/mello/commander/projects/skool-api/`

## Competitor Etsy Shops (referenced by Alec)
- **NorthPrints** -- $5.9K/mo, 31 listings, European vintage oils, dark academia, 4.97 rating
- **AtlasVintagePrints** -- $1.1K/mo, 11 listings, cottagecore animals (birds/bunnies), 4.99 rating
- **AntiqueWhiteArt** -- $460/mo, 3 listings, spring wildflowers, 3.32 rating

## What Sells (from Alura data, 2026-03-28)
- Moody vintage oil paintings, muted earth tones
- Gallery wall art SETS at premium pricing ($16+)
- Cottagecore animals, botanicals, landscapes
- Samsung Frame TV art (emerging)

**How to apply:** When generating art for challenge or Etsy, use the `art-prompt-builder` skill which pulls proven prompts from NocoDB first.
