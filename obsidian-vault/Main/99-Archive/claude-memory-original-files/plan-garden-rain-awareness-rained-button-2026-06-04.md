---
name: PLAN: Garden rain-awareness + Rained button (2026-06-04)
description: Full implementation plan for the mello-garden rain7d net + POST /api/water/rained + Telegram/web Rained button (built & shipped 2026-06-04)
type: reference
---

<!-- REVIEWED -->
# Garden: Rain Awareness + "Rained" Quick Action

Two existing projects:
- Web app: `/home/mello/mello-garden` (Next.js 14 App Router + Prisma + PostgreSQL; container `mello-garden`, host `127.0.0.1:3010` -> container `:3000`; public `https://garden.synai.ai`).
- Telegram bot: `/home/mello/commander/projects/garden-telegram` (python-telegram-bot; container `garden-telegram`; talks to web via `X-Internal-Token`, base `http://mello-garden:3000`).

Goal: stop the watering recommender from saying "water" after a multi-day rain that ended >48h ago, and give Roberto a one-tap "Rained" override next to "Water All" in Telegram (he visually confirms rain on camera, then taps it).

---

## Current State Summary

### The bug (confirmed by reading the code)
`lib/watering.js` `getWateringAdvice()`:
1. Only reads `weather.rain48h` (line 56). `lib/weather.js` already computes and returns `rain7d` (`processWeatherData`, lines 105-114, 164) but `getWateringAdvice` never reads it. Rain older than 48h is invisible to the algorithm.
2. The "last watered" clock (`daysSinceWatered`, lines 66, 82-85) is derived solely from non-skipped `WaterLog` rows (`app/api/watering/status/route.js` lines 18-26 query `waterLogs` `where: { skipped: false }`, take 1, newest). Rain never writes a log, so with no manual watering during a rainy week `daysSinceWatered` keeps climbing (29d observed) and trips `status='water'`.

### Schema (no migration needed)
`prisma/schema.prisma` `WaterLog` already has free-text `method` and `reason` (lines 54, 56) plus `amount`, `tempF`, `humidity`, `notes`, `loggedAt`. A rain event is just a `WaterLog` with `method='rain'`. The status route's "last watered" query treats any `skipped:false` row as a watering, so a rain log naturally resets the clock with zero schema change.

### Plant population (drives the "outdoor" decision -- IMPORTANT)
`prisma/seed.js` has 8 plants. Six are `container=true` (Fig, Lime, Jabuticaba, Avocado, Goiaba, Peach) but all are physically OUTSIDE in pots. Only two are `container=false`: Indian Hawthorns (in-ground) and Wisteria (`waterNeeds='none'`).

Consequence: the literal spec definition "outdoor = `container=false && waterNeeds!='none'`" would match ONLY the Indian Hawthorns -- a single plant -- and rain would not reset the 6 potted trees that are the whole point. Roberto explicitly said "most of Roberto's plants are outside."

Decision (locked, see Open Decisions for rationale): **"Rain-exposed" = active plant with `waterNeeds != 'none'`** (i.e. everything except Wisteria), NOT filtered by `container`. There is no indoor/location field today; potted trees are outdoors. The endpoint also accepts an explicit `plantIds` override so callers can scope it if that ever changes.

### Auth / wiring
- `middleware.js`: a request passes if it has a valid iron-session cookie OR header `x-internal-token === process.env.GARDEN_INTERNAL_TOKEN` (lines 28-33). New `/api/water/rained` is under `/api/` and inherits this automatically. No middleware change.
- Bot callbacks: `bot.py` registers ONE catch-all `CallbackQueryHandler(handle_callback)` (line 146). There are NO per-pattern handlers. Dispatch happens by prefix inside `handlers/callbacks.py` `handle_callback` (lines 42-63). So the "Rained" callback is added as a new prefix branch there, NOT as a new handler in `bot.py`. (This corrects the task brief, which assumed `gbw`/`gbwc` are registered in `bot.py`.)
- `garden_api.py` (`GardenAPI`): `_request`, `bulk_water` (POST `/api/water/bulk` `{plantIds}`), `water_plant`, etc. Bot sends `X-Internal-Token` header (line 21).
- `formatters.py` `format_watering_digest` (lines 30-94) builds the digest text + button matrix, ending with a `Refresh` button (line 91). This digest is used by `/status` (commands.py 66-71), refresh (callbacks.py 138-146), and the 7am `morning_digest` (scheduler.py 58-67). Adding "Rained" to this button row gives it coverage in all three places at once.
- `cmd_water_all` (commands.py 188-220) only builds a keyboard when plants have `status=='water'`; if nothing needs water it returns early with "No plants need watering right now." So "Rained" must NOT live only inside `cmd_water_all` (Roberto wants to log rain proactively even when nothing shows red). Primary home = the digest button row; `cmd_water_all` gets a parallel "Rained" button when it does render.

### Tooling gaps (Phase 0 must close these)
- `package.json` has NO test runner and NO `test` script, and NO `zod`. devDeps are only Next/Tailwind/Prisma tooling.
- `lib/watering.js` uses CommonJS `module.exports`. Cleanest test runner with zero new deps and zero transform config: **Node's built-in `node --test`** (Node 18+, and the Dockerfile base is `node:20-alpine`). Tests live in `lib/__tests__/*.test.js` using `require()`.
- `zod`: not present. The new route needs Zod per the coding rules. Adding `zod` to `dependencies` means `package-lock.json` MUST be regenerated locally before the Docker build, because the Dockerfile uses `npm ci` (Dockerfile line 6), which fails if lockfile and package.json disagree.

---

## Open Decisions (resolved in this plan)

1. **Which plants does "Rained" reset?** -> All active plants with `waterNeeds != 'none'` (excludes Wisteria only). Rationale: 6 of 8 plants are potted-but-outside; filtering by `container=false` would reset only 1 plant and miss the trees that actually sit in the rain. The endpoint additionally accepts optional `plantIds` to override the default selection.
2. **`rain7d` automatic safety net -- suppress or downgrade?** -> Downgrade-only, and only when the per-tier `rain48h` fast-path did not already skip. If 7-day rain is high (>= `rain7dSkip`), a would-be `water` becomes `check` (yellow) with a rain reason, rather than a hard `skip`. Reason: 7-day-old rain means soil is probably still moist but not guaranteed wet today; "check soil" is the safe, non-alarming state. The existing `rain48h` hard-skip is unchanged (recent rain = confident skip).
3. **Per-tier `rain7dSkip` thresholds (Hoover, AL).** Add a `rain7dSkip` to each `THRESHOLDS` tier. Values chosen so a normal rainy week (~1"+) suppresses the red state for low/medium plants while thirsty `medium-high` plants in containers still get flagged sooner:
   - `none`: 999 (unused)
   - `low-medium`: 0.8"
   - `medium`: 0.6"
   - `medium-high`: 0.5"
   These are deliberately a few× the 48h `rainSkip` because they cover 7 days, not 2.
4. **Does the rain WaterLog set `amount`?** -> `amount = 'rain'` (free-text string field; the column is `String?`). Store optional measured inches in `notes` (e.g. `"Rain logged via Telegram (~0.5in, ~6h)"`). This avoids overloading `amount` (which elsewhere holds 'moderate'/'light') with a number while still capturing what Roberto reports. `reason` = `"Rain (manual confirm)"`.
5. **Camera / CV** -> OUT OF SCOPE. `lib/vision.js` exists for a future phase; this plan is a manual flow only. No `lib/vision.js` import anywhere in this work.

---

## Prerequisites (Phase 0 -- Run First)

### Required Packages / Tooling
| Package | Version | Where | Status | Notes |
|---|---|---|---|---|
| `zod` | ^3.23 | mello-garden `dependencies` | ADD | Validate `/api/water/rained` body. Must regen lockfile. |
| Node test runner | built-in (`node --test`) | mello-garden devtime | USE | No install. Node 20 in Dockerfile, Node 18+ on host. CommonJS-compatible. |
| python-telegram-bot, httpx, apscheduler | existing | garden-telegram | OK | Already in the image; no new Python deps. |

No new Docker images. No Prisma migration (reuses existing `WaterLog.method`/`reason`/`amount`).

### Commands to run before any code change
```bash
# 1. Confirm host Node supports node --test (need >= 18)
node --version

# 2. Add zod and regenerate the lockfile so the Docker `npm ci` build won't fail
cd /home/mello/mello-garden
npm install zod@^3.23        # updates package.json + package-lock.json
# (sanity) ensure both files now reference zod
grep -n '"zod"' package.json package-lock.json | head

# 3. Confirm GARDEN_INTERNAL_TOKEN is set (needed for curl verification later)
grep -n 'GARDEN_INTERNAL_TOKEN' /home/mello/.env >/dev/null && echo "token present" || echo "MISSING -- stop and ask"
```

### Verification of Phase 0
- `node --version` >= v18.
- `package.json` dependencies include `zod`; `package-lock.json` mentions `zod` (so `npm ci` in Docker will resolve it).
- `GARDEN_INTERNAL_TOKEN` exists in `/home/mello/.env`.

---

## Phase 1 -- Watering algorithm: use `rain7d` (+ tests)

### 1a. `lib/watering.js` -- add `rain7dSkip` to thresholds
Edit `THRESHOLDS` (lines 4-9) to add a `rain7dSkip` per tier:
```js
const THRESHOLDS = {
  'none':        { rainSkip: 999,  dryDays: 999, rain7dSkip: 999 },
  'low-medium':  { rainSkip: 0.3,  dryDays: 5,   rain7dSkip: 0.8 },
  'medium':      { rainSkip: 0.25, dryDays: 3,   rain7dSkip: 0.6 },
  'medium-high': { rainSkip: 0.2,  dryDays: 2,   rain7dSkip: 0.5 },
}
```

### 1b. `getWateringAdvice` -- read `rain7d`, downgrade red -> yellow
- Line 56: destructure `rain7d` too, default 0 when undefined for backward-compat:
  `const { rain48h, rain7d = 0, todayRainProb } = weather`
- Keep the existing `rain48h >= threshold.rainSkip` hard-skip block (lines 57-63) UNCHANGED (recent-rain fast path).
- After the base status is computed (after line 94, before the "Rain forecast override" block at line 96) add a 7-day safety net that only fires when status is the hard `water`:
```js
// 7-day rain safety net: recent-ish rain likely left soil moist.
// Downgrade a hard "water" to "check" (don't hard-skip on week-old rain).
if (status === 'water' && rain7d >= threshold.rain7dSkip) {
  status = 'check'
  color = 'yellow'
  reason = `${rain7d}" rain in last 7d - likely still moist, check soil`
}
```
- Interaction notes (must be preserved by test cases):
  - This sits BEFORE the existing `todayRainProb > 60` downgrade (lines 97-101) and BEFORE the hot-container escalation (lines 104-110). That ordering is intentional: a hot, bone-dry container should still be allowed to re-escalate to `water` even if 7-day rain was high (the `rain48h < 0.1` guard on line 104 means a real recent dry spell still wins). Document this in a test.
  - Winter-dormancy early returns (lines 41-53) are untouched.

### 1c. (optional, low-risk) `getDashboardRecommendations`
Add one recommendation when `rain7d` is high but `rain48h` is low, so the dashboard explains why nothing is red:
```js
// near the rain checks (after line 144)
if (rain48h < 0.1 && rain7d >= 0.6) {
  recs.push(`No rain in 48h but ${rain7d}" fell this week - soil likely still moist.`)
}
```
Keep it additive; do not remove existing recs.

### 1d. Tests (RED -> GREEN -> REFACTOR) -- `lib/__tests__/watering.test.js`
Use `node:test` + `node:assert/strict`, `require('../watering')`. Cover at least:
1. **Repro of the bug (RED first):** `medium` plant, `lastWateredDate` = 29 days ago, `weather = { rain48h: 0, rain7d: 1.2, todayRainProb: 0 }` -> expect `status === 'check'` (was `'water'` before the fix). Write this test FIRST and confirm it fails against current code.
2. `rain48h` hard-skip still wins: `rain48h: 0.3`, `rain7d: 0` -> `status === 'skip'` (unchanged behavior).
3. Low 7-day rain does NOT rescue a dry plant: `rain48h: 0, rain7d: 0.1`, 29d -> `status === 'water'`.
4. Per-tier threshold: `medium-high` plant with `rain7d: 0.55` (>= 0.5) downgrades; `low-medium` with `rain7d: 0.55` (< 0.8) does NOT (stays `water`).
5. Hot dry container still escalates despite high `rain7d`: `container:true`, `current.tempF: 90`, `rain48h: 0`, `rain7d: 1.5`, recently watered -> ends `status === 'water'` (hot-container block re-escalates).
6. `none` waterNeeds -> always `skip` regardless of rain.
7. Backward-compat: weather object WITHOUT `rain7d` key behaves exactly as today (no crash; `rain7d` defaults 0).
8. `getWateringGrid` passes `rain7d` through (shape check) and still returns `daysSinceWatered`.

Add a `test` script to `package.json`:
```json
"scripts": { "test": "node --test" }
```
Run: `cd /home/mello/mello-garden && npm test`. Target: every changed branch in `getWateringAdvice` exercised (>= 80% on changed code). Refactor only after green.

> Note: `node --test` with no path auto-discovers `**/*.test.js` and WILL pick up the many `node_modules/.../**.test.js` files (confirmed present, e.g. `node_modules/next/dist/trace/trace.test.js`). MUST scope discovery to the lib tests: `"test": "node --test lib/__tests__/"`. Run from the repo root (`cd /home/mello/mello-garden && npm test`). Do not run a bare `node --test`.

---

## Phase 2 -- `POST /api/water/rained`

New file `app/api/water/rained/route.js`. Mirrors `app/api/water/bulk/route.js` (Promise.all of `waterLog.create`, auto-capture weather) but selects rain-exposed plants server-side and tags them as rain.

Behavior:
1. Parse body (may be empty) with `await request.json().catch(() => ({}))`.
2. Validate with Zod (all optional):
```js
import { z } from 'zod'
const RainedSchema = z.object({
  hours: z.number().int().min(1).max(168).optional(),   // how long it rained
  amount: z.number().min(0).max(20).optional(),         // measured inches, optional
  plantIds: z.array(z.string()).optional(),             // override selection
}).strict()
```
Wrap `RainedSchema.safeParse(...)`; on failure return `400` with a descriptive (non-sensitive) message.
3. Determine target plants:
   - If `plantIds` provided -> use them.
   - Else query `prisma.plant.findMany({ where: { active: true, waterNeeds: { not: 'none' } }, select: { id: true } })` and map to ids. (This is the "rain-exposed = everything but Wisteria" rule.)
   - If empty -> return `200 { count: 0, message: 'No rain-exposed plants.' }`.
4. Auto-capture weather (try/catch, same as bulk) for `tempF`/`humidity`.
5. Build a human note: `Rain logged via API${amount? ` (~${amount}in)`:''}${hours? ` over ~${hours}h`:''}`.
6. `Promise.all` create one `WaterLog` per plant:
```js
{ plantId, amount: 'rain', method: 'rain', skipped: false, reason: 'Rain (manual confirm)', tempF, humidity, notes }
```
   (Immutability: build each `data` object fresh inside `.map`; no mutation.)
7. Return `201 { count, plantIds, loggedAt }`.
8. Wrap the whole handler in try/catch; `console.error('Rained log error:', error)` and `500 { error: 'Failed to log rain' }`. No secret leakage in messages.

Auth: inherited from `middleware.js` (cookie OR `x-internal-token`); no change.

Why this design: reuses the exact write pattern the rest of the app uses, resets the "last watered" clock for all rain-exposed plants via the existing `skipped:false` newest-log query in the status route, and needs no migration.

---

## Phase 3 -- Bot "Rained" button + handler

### 3a. `garden_api.py` -- add `rained()`
After `bulk_water` (line 74):
```python
async def rained(self, hours: int | None = None, amount: float | None = None) -> dict:
    payload = {}
    if hours is not None:
        payload["hours"] = hours
    if amount is not None:
        payload["amount"] = amount
    return await self._request("POST", "/api/water/rained", json=payload)
```
(Empty `{}` body is valid; route handles it.)

### 3b. `state.py` -- pending "rained" confirmation (mirror bulk-water)
Add a `rained_pending` dict so a tap shows a confirm step (prevents accidental fat-finger clock resets), reusing the exact pattern of `bulk_water_pending`:
- Add `"rained_pending": {}` to `DEFAULT_STATE` (line 12-18).
- Add `RAINED_EXPIRY_MINUTES = 5`.
- Add `add_rained_pending(callback_id, payload)`, `get_rained_pending(callback_id)` (with staleness check), `remove_rained_pending(callback_id)`, and include rained keys in a cleanup (extend `cleanup_stale_bulk_water` or add `cleanup_stale_rained`; call it from `post_init` alongside the existing cleanups in `bot.py` lines 81-82).

> Simpler alternative (acceptable): skip the pending/confirm step and make the first tap open a small inline confirm built inline (no state needed) -- but reusing the state pattern keeps parity with bulk-water and survives restarts. Default: use state.

### 3c. `formatters.py` -- add "Rained" to the digest button row
In `format_watering_digest`, change the final controls row (line 91) from just Refresh to Refresh + Rained:
```python
buttons.append([
    InlineKeyboardButton("\U0001f504 Refresh", callback_data="gref:status"),
    InlineKeyboardButton("\U0001f327 Rained", callback_data="grn"),   # cloud-rain emoji
])
```
`grn` = "garden rained" (no args; server picks rain-exposed plants). This makes "Rained" appear in `/status`, the refresh re-render, and the 7am morning digest with no extra wiring (all three call `format_watering_digest`).

### 3d. `commands.py` -- add "Rained" next to "Water All"
In `cmd_water_all`, when it renders the confirm keyboard (lines 210-215), add a Rained button so it sits literally next to Water All as Roberto asked:
```python
InlineKeyboardButton("\U0001f327 Rained", callback_data="grn"),
```
Also: when `cmd_water_all` finds nothing needy (line 199-200), instead of only "No plants need watering right now." attach a one-button keyboard `[[Rained]]` so he can still log rain from that command. (Keeps the proactive path.)

### 3e. `handlers/callbacks.py` -- dispatch + confirm + execute
Add prefix branches in `handle_callback` (the if/elif chain, lines 42-63):
```python
elif data == "grn":
    await _rained_prompt(query, context)
elif data.startswith("grnc:"):
    await _rained_confirm(query, context, data[5:])
elif data == "grnx":
    await _rained_cancel(query, context)
```
New helpers (mirror `_bulk_water_*`):
```python
async def _rained_prompt(query, context):
    # create a pending entry, show confirm/cancel as a NEW message.
    # Do NOT edit the digest's reply_markup here: that would wipe the per-plant
    # Water/Skip buttons. Send a separate confirm message instead.
    callback_id = uuid.uuid4().hex[:12]
    persistent_state.add_rained_pending(callback_id, {})   # no measured amount for one-tap
    kb = InlineKeyboardMarkup([[
        InlineKeyboardButton("✅ Yes, it rained", callback_data=f"grnc:{callback_id}"),
        InlineKeyboardButton("❌ Cancel", callback_data="grnx"),
    ]])
    await query.answer()
    await query.message.reply_text(
        "\U0001f327 Log rain for all outdoor plants? This resets their watering clock.",
        reply_markup=kb,
    )

async def _rained_confirm(query, context, callback_id):
    entry = persistent_state.get_rained_pending(callback_id)
    if entry is None:
        await query.answer("Expired. Tap Rained again.", show_alert=True); return
    api = _get_api(context)
    try:
        result = await api.rained()
        persistent_state.remove_rained_pending(callback_id)
        count = result.get("count", 0)
        await query.answer(f"\U0001f327 Logged rain for {count} plants")
        await query.edit_message_text(f"\U0001f327 Logged rain. {count} outdoor plants reset - they won't show as needing water.")
    except Exception as e:
        await query.answer(f"Error: {e}", show_alert=True)

async def _rained_cancel(query, context):
    await query.answer("Cancelled")
    try:
        await query.edit_message_text("Cancelled.")   # this edits the confirm msg, not the digest
    except Exception:
        pass
```
Notes:
- `uuid` is imported in commands.py; add `import uuid` to callbacks.py.
- **Emoji style:** the existing bot files use `\Uxxxxxxxx` escape sequences (e.g. `\U0001f4a7`), not raw emoji literals. Match that style in the real code (use `\U0001f327` for the rain cloud, `✅`/`❌` for check/cross). Raw emoji are shown above only for plan readability.
- The confirm flow runs on a SEPARATE message (`_rained_prompt` sends a new message; confirm/cancel edit that message), so the original digest keeps its per-plant Water/Skip buttons intact.

> Future option (documented, not built now): a `/rained <hours> <inches>` command that passes measured values to `api.rained(hours, amount)`. Out of scope for v1 one-tap.

### 3f. `bot.py`
No new `CommandHandler`/`CallbackQueryHandler` needed (the catch-all already routes `grn*`). If 3b adds a `cleanup_stale_rained`, call it in `post_init` next to lines 81-82. Optionally add a `/rained` `BotCommand` description if a future command is added (skip for v1).

---

## Phase 4 -- (Optional) Web dashboard "Rained" button

`app/page.js` already has handlers like `handleBulkWater` (lines 94-103) and renders `QuickLogFAB`. Add:
```js
async function handleRained() {
  const res = await fetch('/api/water/rained', {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({}),
  })
  if (res.ok) { await fetchData() }   // refresh grid so reset is visible
}
```
Render a small "Rained" button near the Watering Status heading (line 242-246) or inside `QuickLogFAB`. Keep it additive; verify in browser (Rule 5). This phase is optional and can ship after Phases 1-3 are verified.

---

## Phase 5 -- Build + Verify both containers

Per CLAUDE.md, Docker changes need full rebuild, not restart.

### Build
```bash
cd /home/mello

# Web app (Phases 1,2,4)
docker stop mello-garden && docker rm mello-garden
docker compose up -d --build mello-garden

# Bot (Phase 3) -- after mello-garden is healthy (bot depends_on service_healthy)
docker stop garden-telegram && docker rm garden-telegram
docker compose up -d --build garden-telegram
```

> Weather cache note: `fetchCurrentWeather` caches for 15 min in-process. The rebuild restarts the container, so the cache starts empty and the new `rain7d` logic is in effect immediately. Also, the visible "no longer needs water" result after `/api/water/rained` comes from the DB clock reset (status route re-queries newest `WaterLog`), so it is independent of the weather cache.

### Verify -- web API (server-side curl; token from env)
```bash
TOKEN="$(grep -E '^GARDEN_INTERNAL_TOKEN=' /home/mello/.env | cut -d= -f2-)"

# health
curl -s -H "x-internal-token: $TOKEN" http://127.0.0.1:3010/api/health

# status BEFORE: capture any plant currently status=water + the weather.rain7d value
curl -s -H "x-internal-token: $TOKEN" "http://127.0.0.1:3010/api/watering/status?tz=America/Chicago" \
  | python3 -c "import sys,json;d=json.load(sys.stdin);print('rain48h',d['weather']['rain48h'],'rain7d',d['weather']['rain7d']);print([(g['plant']['name'],g['status']) for g in d['grid']])"

# fire the rain endpoint (one-tap, empty body)
curl -s -X POST -H "x-internal-token: $TOKEN" -H "Content-Type: application/json" \
  -d '{}' http://127.0.0.1:3010/api/water/rained

# status AFTER: rain-exposed plants should now be skip/check, not water; daysSinceWatered ~0
curl -s -H "x-internal-token: $TOKEN" "http://127.0.0.1:3010/api/watering/status?tz=America/Chicago" \
  | python3 -c "import sys,json;d=json.load(sys.stdin);print([(g['plant']['name'],g['status'],g['daysSinceWatered']) for g in d['grid']])"

# Zod validation negative test (should 400)
curl -s -o /dev/null -w '%{http_code}\n' -X POST -H "x-internal-token: $TOKEN" \
  -H "Content-Type: application/json" -d '{"hours":999}' http://127.0.0.1:3010/api/water/rained
```
Expected: rain logs created (`count` > 0), every rain-exposed plant flips off `water`, `daysSinceWatered` resets near 0, and `{"hours":999}` returns `400`.

### Verify -- web UI (Rule 5)
Use browser-agent against `https://garden.synai.ai` (NOT localhost in any user-facing note): load the dashboard, confirm no plant card shows red "water" after the rain log, and (Phase 4) the "Rained" button is visible and works.

### Verify -- bot (live)
- `docker logs --tail 50 garden-telegram` shows clean start, API health OK, no callback errors.
- In Telegram: `/status` -> confirm a `🌧 Rained` button sits next to `🔄 Refresh`. Tap it -> confirm prompt -> Yes -> success message with a plant count.
- `/water_all` -> confirm `🌧 Rained` sits next to `💧 Water All`. With nothing needy, confirm the standalone Rained button appears.
- Re-run `/status` -> previously-red plants now show green/yellow.

### Unit tests
```bash
cd /home/mello/mello-garden && npm test     # node --test lib/__tests__/, all green, bug-repro test passes
```

---

## Rollback

- Code: `git -C /home/mello/mello-garden checkout -- lib/watering.js app/api/water/rained/route.js app/page.js package.json package-lock.json` and `git -C /home/mello/commander/projects/garden-telegram checkout -- garden_api.py state.py formatters.py handlers/callbacks.py commands.py bot.py`, then rebuild both containers with the same `stop && rm && compose up -d --build` commands.
- Data: rain events are ordinary `WaterLog` rows. To undo a bad rain log, delete rows by tag:
  `docker exec n8n-postgres psql -U n8n -d mello_garden -c "DELETE FROM \"WaterLog\" WHERE method='rain' AND \"loggedAt\" > now() - interval '1 hour';"`
- No migration was applied, so there is nothing to revert at the schema level.

---

## Files Touched (summary)

mello-garden:
- `lib/watering.js` (THRESHOLDS + `getWateringAdvice` rain7d net + optional rec)
- `lib/__tests__/watering.test.js` (new)
- `app/api/water/rained/route.js` (new)
- `package.json` (`zod` dep, `test` script) + `package-lock.json` (regen)
- `app/page.js` (optional Phase 4 button)

garden-telegram:
- `garden_api.py` (`rained()`)
- `state.py` (`rained_pending` helpers)
- `formatters.py` (digest button)
- `commands.py` (water_all button + empty-state button)
- `handlers/callbacks.py` (`grn`/`grnc:`/`grnx` branches + helpers)
- `bot.py` (only if a `cleanup_stale_rained` is added)

---

## Review Notes

The automated 4-musketeers consensus hook did not run in this subagent execution environment (no consensus file was produced and no review section was appended; ExitPlanMode/EnterPlanMode are likewise unavailable here). In its place I ran a split-role self-review (web-route reviewer, bot reviewer, test reviewer) and applied the findings below. The orchestrator that invoked this agent should still surface the plan for approval before implementation.

Findings incorporated:
- **CRITICAL (bot UX bug):** original draft had `_rained_prompt` call `query.edit_message_reply_markup` on the digest, which would have wiped every per-plant Water/Skip button and replaced them with the confirm pair. Fixed: the confirm prompt is now sent as a NEW message; confirm/cancel edit that message, leaving the digest intact.
- **HIGH (broken tests):** a bare `node --test` discovers `node_modules/**/*.test.js` (verified those files exist). Pinned the script to `node --test lib/__tests__/` and added an explicit "do not run bare `node --test`" warning.
- **HIGH (Docker build break):** adding `zod` without regenerating `package-lock.json` would fail the image build (Dockerfile uses `npm ci`). Made lockfile regeneration an explicit Phase 0 step with a grep check.
- **HIGH (wrong plant selection):** the literal spec rule `container=false && waterNeeds!='none'` would reset only the single in-ground Indian Hawthorns (6 of 8 plants are potted-but-outside). Changed the rule to "active AND `waterNeeds!='none'`" (everything but Wisteria), with an optional `plantIds` override. Documented in Open Decisions #1 with the seed-data evidence.
- **MEDIUM (style consistency):** the bot codebase uses `\Uxxxxxxxx` emoji escapes, not raw emoji. Added a note to use escapes in real code; raw emoji in the plan are for readability only.
- **MEDIUM (algorithm interaction):** clarified ordering so the 7-day downgrade runs before the `todayRainProb` and hot-container blocks, and added explicit test cases (hot dry container re-escalates despite high `rain7d`; low 7-day rain does not rescue a dry plant).
- **MEDIUM (verification realism):** added a weather-cache note explaining the rebuild clears the 15-min cache and that the clock reset is DB-driven (independent of cache).

Dismissed / out of scope:
- Computer-vision rain auto-detection (`lib/vision.js`): explicitly out of scope per the request; manual confirm only.
- Adding jest/vitest: rejected in favor of built-in `node --test` to avoid new deps + transform config in a Next app for pure-function tests.
- A `/rained <hours> <inches>` measured command: noted as a future option; v1 is one-tap with optional body fields already supported by the endpoint.
- Prisma migration for an `outdoor`/`location` field: not needed for v1 (no migration at all). Noted as a possible future field if a truly-indoor plant is ever added.

## Team Structure
- **Lead / web app (Next.js + Prisma):** owns Phase 1 (algorithm + tests), Phase 2 (`/api/water/rained`), Phase 4 (dashboard button), and the mello-garden rebuild + curl/browser verification. Strong on Next.js App Router route handlers, Prisma queries, and Zod.
- **Bot engineer (python-telegram-bot):** owns Phase 3 (garden_api/state/formatters/commands/callbacks) and the garden-telegram rebuild + live Telegram verification. Must understand the single catch-all `CallbackQueryHandler` dispatch model and the JSON `state.py` pattern.
- **Reviewer (code-reviewer agent):** runs after Phases 1-3 per quality-gates rule (multi-file change). Checks immutability, try/catch with descriptive errors, Zod usage, no secret leakage, no `localhost` in user-facing strings.
- Phases 1 and 2 are sequential (route depends on algorithm being correct/tested). Phase 3 depends on Phase 2 being deployed (bot calls the live endpoint). Phase 4 is independent of Phase 3 and optional. Single implementer can do all phases in order; the split above is for parallelization if two agents are used (web vs bot) once Phase 2 is merged.
