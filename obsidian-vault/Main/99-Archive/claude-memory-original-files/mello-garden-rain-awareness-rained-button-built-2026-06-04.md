---
name: Mello Garden: rain-awareness + Rained button (built 2026-06-04)
description: Garden app now rain-aware: rain7d net + POST /api/water/rained + Telegram/web Rained button; 3 recovery trees set to medium with summer feeding reminders
type: project
---

Built the rain-awareness feature for **mello-garden** (web, container `mello-garden`, 127.0.0.1:3010 -> garden.synai.ai) and **garden-telegram** bot.

**What it does**
- `lib/watering.js`: added per-tier `rain7dSkip` to THRESHOLDS (low-medium 0.8", medium 0.6", medium-high 0.5") and a 7-day rain "safety net" in `getWateringAdvice` that downgrades a hard `water` -> `check` when `rain7d >= rain7dSkip`. Runs BEFORE the todayRainProb and hot-container blocks, so a hot dry container still re-escalates. Fixes the "29 days since watered after a rainy week" bug.
- `lib/weather.js`: `rain7d` already computed from Open-Meteo daily; fixed its filter to compare date strings (`daily.time[i] <= todayStr`) instead of parsing date-only as UTC midnight.
- NEW `app/api/water/rained/route.js`: Zod-validated POST (`hours?`, `amount?`, `plantIds?`, `.strict()`). Empty `{}` body = reset ALL rain-exposed plants. **Rain-exposed = active AND `waterNeeds != 'none'`** (everything but Wisteria), NOT filtered by `container` (6 of 8 plants are potted-but-outside, so container flag is misleading). Writes one `WaterLog{method:'rain', amount:'rain', reason:'Rain (manual confirm)', skipped:false}` per plant; the existing newest-`skipped:false`-log query resets each plant's clock. No schema migration.
- `app/page.js`: "It rained" button in the Watering Status header -> `handleRained()` -> POST then refresh.
- Bot: `garden_api.rained()`; `state.py` `rained_pending` helpers (mirror bulk_water); `formatters.py` adds `grn` "Rained" button to the digest row; `commands.py` adds it next to Water All + a standalone one in the empty state; `handlers/callbacks.py` dispatches `grn`/`grnc:`/`grnx` (confirm prompt is a NEW message so the digest's per-plant buttons survive); `bot.py` calls `cleanup_stale_rained`.

**Tooling**: added `zod` (^3.23) + `"test": "node --test lib/__tests__/*.test.js"` to package.json (regen lockfile since Dockerfile uses `npm ci`). Tests in `lib/__tests__/watering.test.js` (9, all green). Node 24 `node --test <dir/>` fails (treats dir as a module) -> use the glob.

**Recovery trees** (American Holly, Chinese Fringe Flower/Loropetalum, Fragrant Tea Olive): set `waterNeeds='medium'` (was low-medium) for a growth push; added 4 `fertilizing` TaskLog reminders (Holly-Tone + seaweed/fish, Jun 7 -> Jul 15, then stop). See [[garden-cold-damaged-evergreens-fruit-trees-hoover-al]].

**Ops notes**
- To undo erroneous rain logs: `DELETE FROM "WaterLog" WHERE method='rain' AND "loggedAt" > now() - interval '15 minutes';` (DB `mello_garden` on `n8n-postgres`).
- KNOWN ISSUE: garden-telegram's httpx INFO logging prints the full Telegram API URL incl. the bot token on every request (`docker logs garden-telegram`). Pre-existing; consider quieting httpx logging.
