"""tokens-savings dashboard backend.

Serves index.html at / and aggregated per-model RTK savings as JSON at /stats.
Data source: Postgres `rtk.commands` (model column is populated — no transcript
scan needed). Read-only.
"""

import os
import sys
from datetime import datetime, timedelta, timezone

import psycopg2
import psycopg2.extras
from flask import Flask, jsonify, request, send_from_directory

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pricing import MODELS, ORDER, bucket, CACHE_WRITE_MULT  # noqa: E402

APP_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DSN = os.environ.get("DATABASE_URL", "postgresql://n8n:n8n@n8n-postgres:5432/rtk")

# Presentation timezone for /stats/timeseries bucket labels (fixed UTC-6, matches
# operator's local time). DB storage/queries remain UTC throughout.
LOCAL_OFFSET = timedelta(hours=-6)
LOCAL_TZ = timezone(LOCAL_OFFSET)

app = Flask(__name__)


def get_conn():
    return psycopg2.connect(DB_DSN)


def fetch_stats():
    with get_conn() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                """
                SELECT model,
                       COUNT(*) AS n,
                       COALESCE(SUM(input_tokens), 0) AS input_tokens,
                       COALESCE(SUM(output_tokens), 0) AS output_tokens,
                       COALESCE(SUM(saved_tokens), 0) AS saved_tokens
                FROM commands
                GROUP BY model
                """
            )
            rows = cur.fetchall()

    agg = {k: {"usage": 0, "compacted": 0, "saved": 0} for k in ORDER}
    unbucketed_n = 0
    total_count = 0
    total_output = 0
    for row in rows:
        total_count += int(row["n"])
        total_output += int(row["output_tokens"])
        key = bucket(row["model"])
        if key is None:
            unbucketed_n += row["n"]
            continue
        agg[key]["usage"] += int(row["input_tokens"])
        agg[key]["compacted"] += int(row["output_tokens"])
        agg[key]["saved"] += int(row["saved_tokens"])

    if unbucketed_n:
        app.logger.warning("fetch_stats: %d rows had no model bucket", unbucketed_n)

    models = []
    total_dollars = 0.0
    total_dollars_cached_write = 0.0
    for key in ORDER:
        m = agg[key]
        price_in = MODELS[key]["in"]
        # Conservative floor: saved tokens valued at list input price.
        dollars = round(m["saved"] * price_in / 1_000_000.0, 2)
        # Realistic baseline: saved tokens would otherwise have entered the
        # prompt cache on write (5-min TTL, priced at CACHE_WRITE_MULT x input).
        # Every later turn also re-reads that context at 0.1x input (untracked
        # here — this field covers the first-write cost only, not the re-reads).
        dollars_cached_write = round(
            m["saved"] * price_in * CACHE_WRITE_MULT / 1_000_000.0, 2
        )
        total_dollars += dollars
        total_dollars_cached_write += dollars_cached_write
        models.append(
            {
                "key": key,
                "name": MODELS[key]["name"],
                "color": MODELS[key]["color"],
                "usage": m["usage"],
                "compacted": m["compacted"],
                "saved": m["saved"],
                "dollars": dollars,
                "dollars_cached_write": dollars_cached_write,
            }
        )

    return {
        "live": True,
        "updated": datetime.now(timezone.utc).isoformat(),
        "count": total_count,
        "output_total": total_output,
        "models": models,
        "totals": {
            "dollars": round(total_dollars, 2),
            "dollars_cached_write": round(total_dollars_cached_write, 2),
        },
    }


def fetch_timeseries(granularity, rng):
    """Zero-filled per-model saved/usage buckets for the last `rng` day/hour slots.

    Bucketing is done in Python against LOCAL_TZ (fixed UTC-6) so bucket
    boundaries line up with the operator's "today"/"yesterday". The DB query
    itself stays a plain UTC range scan (read-only, indexed on timestamp).
    """
    now_utc = datetime.now(timezone.utc)
    now_local = now_utc.astimezone(LOCAL_TZ).replace(tzinfo=None)

    if granularity == "hour":
        cur_bucket_local = now_local.replace(minute=0, second=0, microsecond=0)
        step = timedelta(hours=1)
    else:
        cur_bucket_local = now_local.replace(hour=0, minute=0, second=0, microsecond=0)
        step = timedelta(days=1)

    start_bucket_local = cur_bucket_local - step * (rng - 1)
    # Convert the local bucket start back to an absolute UTC instant for the WHERE clause.
    start_utc = (start_bucket_local.replace(tzinfo=LOCAL_TZ)).astimezone(timezone.utc)

    with get_conn() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                """
                SELECT timestamp,
                       model,
                       COALESCE(input_tokens, 0) AS input_tokens,
                       COALESCE(saved_tokens, 0) AS saved_tokens
                FROM commands
                WHERE timestamp >= %s
                """,
                (start_utc,),
            )
            rows = cur.fetchall()

    bucket_list = [start_bucket_local + step * i for i in range(rng)]
    buckets_by_key = {}
    ordered = []
    for bl in bucket_list:
        entry = {
            "ts": bl.replace(tzinfo=LOCAL_TZ).isoformat(),
            "models": {k: {"saved": 0, "usage": 0} for k in ORDER},
            "total_saved": 0,
        }
        buckets_by_key[bl] = entry
        ordered.append(entry)

    for row in rows:
        row_local = row["timestamp"].astimezone(LOCAL_TZ).replace(tzinfo=None)
        if granularity == "hour":
            bkey = row_local.replace(minute=0, second=0, microsecond=0)
        else:
            bkey = row_local.replace(hour=0, minute=0, second=0, microsecond=0)
        entry = buckets_by_key.get(bkey)
        if entry is None:
            continue  # outside requested window (edge rounding), skip
        key = bucket(row["model"])
        if key is None:
            continue
        entry["models"][key]["saved"] += int(row["saved_tokens"])
        entry["models"][key]["usage"] += int(row["input_tokens"])

    for entry in ordered:
        entry["total_saved"] = sum(m["saved"] for m in entry["models"].values())

    return {
        "granularity": granularity,
        "range": rng,
        "buckets": ordered,
    }


@app.route("/stats")
def stats():
    return jsonify(fetch_stats())


@app.route("/stats/timeseries")
def timeseries():
    granularity = request.args.get("granularity", "day")
    if granularity not in ("day", "hour"):
        return jsonify({"error": "granularity must be 'day' or 'hour'"}), 400

    default_range = 14 if granularity == "day" else 48
    max_range = 90 if granularity == "day" else 168
    try:
        rng = int(request.args.get("range", default_range))
    except (TypeError, ValueError):
        return jsonify({"error": "range must be an integer"}), 400
    rng = max(1, min(rng, max_range))

    return jsonify(fetch_timeseries(granularity, rng))


@app.route("/healthz")
def healthz():
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                cur.fetchone()
        return jsonify({"ok": True}), 200
    except Exception as e:  # noqa: BLE001
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route("/")
def index():
    return send_from_directory(APP_DIR, "index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
