---
name: Etsy Competitor Price Tracker Phase 1 (API-based, no scraping)
description: Etsy Open API v3 nightly tracker (no Lightpanda/DataDome scraping), 3 NocoDB tables, base price + implied discount logic, sale-event detection, Telegram digest, systemd cron at 09:00 UTC
type: project
---

# Etsy Competitor Price Tracker — Phase 1

**Key pivot**: Original plan used Lightpanda scraping. Etsy's DataDome bot protection blocks all headless browsers. Switched to **Etsy Open API v3** which provides full competitor data (price, tags, views, favorites) with zero bot detection risk using Roberto's existing API key.

Read-only competitor intelligence foundation; later sale-intelligence engine will reason over the price history. **Live at `/home/mello/commander/projects/etsy_competitor_tracker/`**, see also [[etsy-competitor-tracker]] (high-level overview).

## Scope (Phase 1)

- 3 NocoDB tables (competitors, listings, price history) in Commander base `ph5ghfzrkyg3yvy`
- Nightly fetcher using Etsy API v3 (no scraping)
- Base price tracking + implied discount % calculation
- Seed script: provide shop slugs → API auto-discovers all their listings
- Telegram nightly digest with sale change alerts

**Out of scope** (deferred): new-competitor auto-discovery via keyword search; pattern analyzer / sale prediction; ANY writes to Etsy; per-variant inventory (requires OAuth).

## Etsy API v3 Endpoints (public, API key only)

Auth: `x-api-key: {ETSY_API_KEYSTRING}:{ETSY_API_SHARED_SECRET}` — no OAuth.

| Endpoint | Purpose | Rate |
|---|---|---|
| `GET /v3/application/shops?shop_name={name}` | Look up shop by name → shop_id | 10 req/s |
| `GET /v3/application/shops/{shop_id}` | Shop metadata (active count, favorites, vacation) | 10 req/s |
| `GET /v3/application/shops/{shop_id}/listings/active?limit=100` | All active listings (paginates) | 10 req/s |
| `GET /v3/application/listings/{listing_id}` | Single listing detail | 10 req/s |

Per-listing fields: `listing_id`, `title`, `price` (amount/divisor/currency), `tags[]`, `num_favorers`, `views`, `quantity`, `url`, `shop_id`, `has_variations`, `state`.

**Important**: API returns the FINAL buyer price (after any discount). There is no `is_on_sale` or `original_price` field. **Sale detection is inferred from price history.**

100 listings across ~20 shops = ~25 API calls total. Under 30 seconds. Way faster than scraping.

## NocoDB Schema

**`etsy_competitors`**: shop_id, shop_slug (unique), shop_name, shop_url, niche, listing_active_count, shop_favorites, added_date, notes, is_active

**`etsy_competitor_listings`**: listing_id (unique), shop_id, title, listing_url, first_seen, last_seen, last_status (`active`|`inactive`|`404`|`api_error`), current_price, **base_price** (highest non-sale price seen), **implied_discount_pct**, currency, is_active

**`etsy_price_history`**: listing_id, date, price, base_price, implied_discount_pct, currency, num_favorites, views, quantity, title, tags (JSON), **event** (`none`|`sale_started`|`sale_ended`|`sale_deepened`|`sale_reduced`|`price_changed`|`title_changed`|`tags_changed`)

## Delta-Only Insertion (keeps history table ≤ 50k rows/year)

A new `etsy_price_history` row is written ONLY when:
- `price` changed
- `implied_discount_pct` changed
- `title` changed
- `tags` changed (sorted JSON comparison)
- `views` changed by >20% (avoids noise from small increments)
- Last row >7 days old (heartbeat)

## Base Price Logic (`pricing.py`)

```python
def compute_base_price(current, prev_base, history):
    """- No history: base = current (first observation = full price)
       - current > prev_base: base = current (price went UP = new full price)
       - current < prev_base and drop >8%: likely sale, KEEP prev_base
       - current < prev_base and drop ≤8%: minor adjustment, update base"""

def compute_implied_discount(current, base):
    return 0 if (base <= 0 or current >= base) else round((1 - current/base) * 100)

def detect_sale_event(prev_pct, new_pct):
    """0→>0 = sale_started; >0→0 = sale_ended; deepened/reduced for >0→>0"""
```

Conservative: only update base upward — self-corrects over time. Phase 2 can backfill.

## Project Layout

```
/home/mello/commander/projects/etsy_competitor_tracker/
├── config.py          # Table IDs, API URLs, timing (no secrets)
├── etsy_fetch.py      # get_shop, get_shop_by_name, get_shop_listings, get_listing
├── pricing.py         # compute_base_price, compute_implied_discount, detect_sale_event
├── nocodb_io.py       # CRUD via curl subprocess + xc-token
├── run_nightly.py     # Orchestrator: fetch all → compute deltas → write → digest
├── seed_competitors.py# YAML of shop slugs → API discovers listings → upsert
├── digest.py          # Telegram message + send via curl
├── bootstrap_tables.py# One-shot: creates 3 tables, persists IDs to config
├── schemas/tables.json
├── seeds/competitors.example.yaml
├── tests/             # test_pricing, test_etsy_fetch, test_nocodb_io
└── cron_run.sh        # Systemd timer entry
```

**Systemd timer**: `OnCalendar=*-*-* 09:00:00 UTC` (3am UTC-6).

## Telegram Digest Shape

```
Etsy Competitor Tracker - 2026-04-06
----
Shops: 20 | Listings: 98/100 active | Duration: 22s

🔻 Sale changes: 4
  AlpineRidgeMugs "Elephant Mug" 0% → 20% off ($14.34 → $11.47, base $14.34)
  ...
📊 Price changes (non-sale): 1
📝 Title changes: 0
🏷️ Tag changes: 2
📈 Top gainer: +42 favorites on MugShopX "Sunset Mug"
```

Truncate if >4096 chars.

## Risks (in order of concern, not all material)

- Listing goes inactive mid-tracking (certain, low impact): API returns state → mark inactive, stop tracking
- Non-USD currencies (certain, low): captured per-row, no conversion in Phase 1
- Base-price misidentification (medium, low): conservative rule + self-correction
- Rate limit (very low, never close to 10 req/s with 1s sleep between shops)
- API key revoked (very low): same key as Roberto's own shops — would notice immediately

## Phase 2 (Future) Hooks Already in Schema

`base_price` column, `event` enum with `sale_deepened`/`sale_reduced`, and per-listing `views` columns let the future sale-intelligence engine reason over sale duration, depth correlation with view spikes, and competitor pricing cycles without schema changes.
