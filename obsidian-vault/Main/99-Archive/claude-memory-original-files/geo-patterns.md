---
name: geo-patterns
description: GEO (Generative Engine Optimization) patterns learned from mellosdesigns.com audit cycle
type: feedback
---

When doing GEO optimization for any site:

1. **SSG pre-rendering is the #1 fix for SPAs** - React Router v7 Framework Mode with `ssr: false` and `prerender` config generates static HTML for every route. AI crawlers see full content instead of empty `<div id="root"></div>`.

2. **JSON-LD schema stacking works** - Multiple schemas per page (Product + HowTo + FAQPage + BreadcrumbList = 4 per product page). Each schema type serves a different AI citation pattern.

3. **FAQ content is the biggest citability lever** - Q&A format with answer-first framing scores highest. Lead with the answer, not context. "ASA is 40% stronger than ABS" beats "Our parts are made from ASA which is..."

4. **Real reviews >> everything for trust signals** - AggregateRating + Review schema with actual Etsy review data massively boosts credibility. Use Etsy API (EtsyClient shop #N, `get_reviews()`) to pull real reviews.

5. **Comparison tables are highly citable** - Stock vs Upgraded tables with specific numbers (MPa, temperatures, lifespan) give AI models structured data to extract and cite.

6. **Meta descriptions must be 150-160 chars** - The GEO audit penalizes both too short and too long. Keep them tight with stats.

7. **llms.txt and ai.txt matter** - Plain text files with site purpose, content locations, and structured data inventory help AI crawlers understand the site.

**Why:** The geo-audit-agent scores on 3 dimensions: Crawler Access (25%), Citability (40%), Technical (35%). Citability is always the bottleneck because it measures content quality, not just presence.

**How to apply:** For any new site GEO audit, run `geo-audit-agent` first, then address in order: crawler access (robots.txt, meta directives), technical (SSR/SSG, JSON-LD, meta tags), then citability (Q&A content, comparison tables, reviews).
