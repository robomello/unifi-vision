---
name: TikTok Shop Victory Plan — Post-Purge Affiliate Strategy (Roberto on-camera)
description: Strategic content factory plan for TikTok Shop affiliate operation (@robomello79): NocoDB schema, hook templates, compliance gates, pilot vs post-grad cadence, gated multi-account path, anti-goals
type: project
---

# TikTok Shop Victory Plan — Post-Purge Window Operation

**Owner**: Roberto de Mello | **Account**: @robomello79 | **Window**: 12–18 months until platform maturity closes the arbitrage.

Premise: the 25% purge of spammy faceless affiliates created an attention vacuum. Veteran earners are on 2–3 month policy-stabilization vacation. Roberto's content factory (~30 videos/month, local Claude CLI, local ComfyUI/LTX-2/Suno/avatar) can ship higher-quality TikTok Shop content faster than 99% of competitors without paying $1,997 for the consultant selling the system Roberto already owns.

## Anti-Goals (explicit)

- DO NOT pay the consultant $1,997.
- DO NOT use OpenAI / Gemini APIs anywhere. Claude CLI only.
- DO NOT use cloud image gen. ComfyUI local only.
- DO NOT replicate banned tactics: identical AI voiceover across accounts, CapCut-template-only videos, faceless reviewer farms, undisclosed affiliate links, "BUY NOW LIMITED TIME".
- DO NOT build multi-account farm yet. Single primary first, prove unit economics.
- DO NOT spread to Shopee/Amazon Live etc until TikTok Shop is profitably ≥ $5k/month for 60 consecutive days.
- DO NOT request samples we have no genuine intent to use.
- DO NOT skip FTC disclosure on a single video. One $51,744 fine wipes a year of profit.

## Hard External Constraints (TikTok policy as of Apr 2026)

- US Affiliate Creator: 1,000+ followers to self-apply; 5,000+ for full Product Marketplace
- Account active 30+ days, consistent posting
- Identity verification mandatory (gov ID)
- **Creator Pilot Program** for <5k followers: locked to products with 95%+ Shop Performance Score; max **5 promo videos + 3 LIVEs per week**. Graduate by 6+ shoppable videos (8s+) OR 1+ livestream (5min+) OR 10 orders, AND ≤1 violation point with 176+ CHR
- 24 violation points / 90 days = ban; repeat violators get instant revocation
- Sample eligibility maintenance: 1+ shoppable video or LIVE in last 120 days
- **FTC**: #ad early in caption + on-screen text + verbal disclosure. Penalties up to $51,744/violation

## Roberto's Unfair Advantages

1. Already on camera weekly — the purge specifically nuked faceless review farms. Real engineer credibility clears the "human signal" bar TikTok's anti-spam ML now demands.
2. Zero marginal cost on AI assets — competitors burn $1–5/video on Veo/Sora/ElevenLabs/Midjourney; Roberto's local stack costs electricity. A/B 5× more variants for same spend.
3. Builder credibility — "controls engineer who runs his own POD shops tests product X" hook the algorithm hasn't seen pumped.
4. Cross-platform repurposing — TikTok Shop video doubles as YT Shorts + IG Reels + Pinterest via channel-factory. One shoot, four surfaces.
5. Engineering instrument-mindedness — NocoDB-backed metrics; affiliate op is a measured-and-tuned system, not an art project.

## NocoDB Schema (`tiktok_shop` base)

Five tables:
- **products**: tiktok_product_id, category (beauty|kitchen|tools|home|fashion|tech|supplements|toys|other), commission_rate, shop_performance_score, price, sample_status (not_requested|requested|approved|denied|shipped|received|filmed|posted), decision_score, notes
- **samples**: tracking_number, cost_to_seller, my_actual_value, shipped/received dates
- **videos**: tiktok_url, hook_template, format (demo|unboxing|before_after|integration|comparison|review), on_camera bool, posted_date, views_24h/7d/30d, clicks_*, sales/gmv/commission, ftc_disclosure_method (caption|onscreen|verbal multi), violation_flag
- **competitors**: tiktok_url, estimated_views, hook_text (Whisper-transcribed), format, what_we_can_beat, scraped_date
- **health**: chr_score, violation_points, shoppable_videos_120d, last_livestream_date, status (pilot|standard|warning|suspended)

## Decision Score (tiktok-trend-scout daily)

```
score = (commission_rate * 10)
      + (gap_opportunity ? 30 : 0)          # <5 affiliate videos in 7d on rising product
      + (price <= $50 ? 15 : 0)             # impulse-buy band
      + category_demonstrability_bonus      # kitchen=15, tools=15, home_org=12, fitness=10, beauty=10, electronics=8, supplements=5, fashion=5
      + roberto_niche_overlap_bonus         # engineering, gadget, kitchen, fitness
      - (shop_performance_score < 95 ? 25 : 0)   # avoid pilot-blocking products
      - saturation_penalty                  # log scale on competitor count
```

Request a sample if ALL: decision_score ≥ 50; commission ≥ 8% (≥10% preferred); shop_perf ≥ 95% (mandatory during pilot); Roberto can credibly demo it; **sample value $20–$200** (below = not worth shoot time; above = enters Refundable Sample territory where seller demands return or GMV milestone — high friction during pilot).

## Hook Templates (post-purge survivors)

1. **Engineer-curiosity** — "I'm a controls engineer — here's what's actually wrong with this $25 [product]"
2. **Day-in-the-life integration** — product in Mercedes job site, 3D-print bench, kitchen, garage
3. **Before/after with measurement** — "I tested for 7 days. Here's the data."
4. **Comparison stack** — "Tested 3 versions. Here's the only one worth $30." (request 3 samples in same category)
5. **Multi-shop angle** — "The [product] I use across all my shops" (selective)
6. **Failure / honest review** — "This failed within a week. Here's why" → drives trust, then promote the alternative
7. **Skill-share** — "I'm an engineer. Here are the 3 [tools] I'd buy starting today"
8. **Process video** — silent/POV use + on-screen subtitle commentary

Banned hook patterns: "I CAN'T BELIEVE THIS PRODUCT" + stock footage, "Buy now before it's gone" (urgency spam), AI voice + overlay text only with no human face, generic CapCut templates shared with other creators.

## Compliance Gates (ship-blocking auto-checks)

Before any video uploads:
- [ ] #ad / #TikTokShop hashtags in first 100 chars of caption
- [ ] On-screen overlay PNG visible frames 0–90 (3s @ 30fps)
- [ ] Verbal disclosure detected (Whisper finds "commission" / "ad" / "paid" in first 15s)
- [ ] No banned-phrase hits in caption ("guaranteed", "miracle", FDA-claim words for non-supplement, urgency spam)
- [ ] Music license clear (Suno only, no copyrighted)
- [ ] No other creator's watermark
- [ ] 1080×1920 vertical, 15–180s

Failure → block upload, ping Roberto with reason.

## Cadence (NOT 3-5/day during pilot)

- **Pilot** (week 1–4 if pilot): 5 product-promo TikTok/week (matches the cap) + 4–6 non-shop videos to keep posting consistency + 1–2 LIVEs/week. **~0.7 product-promo TikToks/day.**
- **Post-graduation**: 5 product-promo TikToks/day = 35/week.
- **Avatar lane caps at 30% of weekly output.** Real-Roberto-on-camera content stays majority — the "human signal" the post-purge algorithm rewards.

## Avatar/Voice-Clone Consent (MANDATORY paper trail)

Before any avatar/cloned-voice output goes live: `/home/mello/commander/projects/tiktok-shop/compliance/likeness-voice-consent.md` with approved likeness/voice model hashes, approved use cases (NO political/financial/health-claim), disclosure requirement ("AI-assisted production" in caption), revocation clause + Roberto's signature.

TikTok 2026 community guidelines require disclosure of "synthetic or manipulated media depicting real people" even when the depicted person is yourself.

## Phase 3 — Multi-Account (gated)

**Trigger**: ≥ $5,000 commission/month for 60 consecutive days AND zero violation points in a 90-day window.

**Fictional personas are NOT viable** — TikTok requires gov-ID identity verification; submitting a fictional identity = identity fraud, criminal liability beyond ToS. Plan rules that out absolutely.

Conservative path (recommended): leverage Roberto's existing shops/brands — 2 strongest get their own account with own legal entity, EIN, phone, payout bank, device/VM, residential IP. Each is genuinely brand-tied. No fingerprint overlap, defensible.

Aggressive path = real human collaborators (network of small business owners or hired creators), filmed at their location, on their device, paid to their bank. Roberto only on orchestration layer (briefs + post-production handoff). Effectively a creator network with explicit 50/50 commission split + Roberto handles tech/editing.

Single-account commission ladder beats multi-account ROI without policy risk: hit Top Creator tier → unlocks higher commission rates + exclusive sellers. Direct seller relationships from DMs after a winning video → custom deals at 12–25% vs marketplace default 5–10%.

## Agents to Build (3 new + 1 extend)

1. `tiktok-trend-scout.md` (haiku) — daily research, n8n cron 7am UTC-6
2. `tiktok-shop-agent.md` (sonnet) — account ops via browser-agent + cookies in `mello/.cookies`; **Phase 1.3.0 feasibility spike first** (test if browser flow is stable, or if Roberto manually clicks Submit while agent generates pitch)
3. `video-compliance-agent.md` (haiku) — FTC checker, Whisper STT for verbal disclosure detection
4. Extend `youtube-uploader-agent` with TikTok mode, or thin `tiktok-uploader-agent` wrapping browser-agent

Rate limits for tiktok-shop-agent (2026 enforcement policy explicitly bans automation tools/scripts): cap 1 action per 30 seconds, max 20 actions per session.

## Critical Path

0.1 → 0.2 (TikTok identity verification, 1–3 days) → 0.7 → 1.1 → 1.4 (sample shipping, 3–7 days) → 2.2 (first shoot) → posted.

**Realistic**: first revenue-generating video ~21 days from kickoff. First $1k commission month ~60 days. First $5k month ~120 days. Phase 3 gate ~6–9 months in.

## Defensive Moat

Compliance is the moat. Quarterly external compliance audit (~$300 paid attorney 1-hour consult) after first $20k earned and every 6 months. Newsletter capture from TikTok traffic = owned audience that survives any single TikTok account ban. NocoDB on Roberto's infra = TikTok losing access doesn't lose data.

## Project Layout

```
/home/mello/commander/projects/tiktok-shop/
  README.md
  notes/{tax-structure.md, policy-summary.md, weekly-review-template.md}
  compliance/{overlay-1080x1920.png, disclosure-3s.wav, caption-template.txt, ftc-checklist.md, likeness-voice-consent.md}
  agents/{tiktok-shop-agent.md, tiktok-trend-scout.md}
  pipelines/{sample-request.n8n.json, video-assembly.n8n.json, weekly-review.n8n.json}
  briefs/YYYY-MM-DD-<product-slug>.md
  shoots/YYYY-MM-DD-<product-slug>/{raw, assembled, assets}
```

See also: [[tiktok-shop-affiliate-operation-robomello79]] and [[tiktok-api-social-posting-orchestrator-state]] for the existing TikTok infrastructure that this plan slots into.
