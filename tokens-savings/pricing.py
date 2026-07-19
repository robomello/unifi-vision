"""Per-model list pricing (USD per 1M tokens) and model-family bucketing.

These are list-price estimates used to value token savings and spend.
Adjust here if official rates differ — the dashboard reads from this table.
"""

# name, color var (matches index.html), price_in, price_out  (USD / 1M tokens)
MODELS = {
    "fable":  {"name": "Fable 5",   "color": "var(--m-fable)",  "in": 10.00, "out": 50.00},
    "opus":   {"name": "Opus 4.8",  "color": "var(--m-opus)",   "in": 5.00,  "out": 25.00},
    "sonnet": {"name": "Sonnet 5",  "color": "var(--m-sonnet)", "in": 3.00,  "out": 15.00},
    "haiku":  {"name": "Haiku 4.5", "color": "var(--m-haiku)",  "in": 1.00,  "out": 5.00},
}
ORDER = ["fable", "opus", "sonnet", "haiku"]

CACHE_READ_MULT = 0.10      # cache read priced at 0.1x input
CACHE_WRITE_MULT = 1.25     # cache creation priced at 1.25x input


def bucket(model_id: str):
    """Map a raw transcript model id -> one of the 4 family keys, or None."""
    if not model_id:
        return None
    m = model_id.lower()
    if "fable" in m:
        return "fable"
    if "opus" in m:
        return "opus"
    if "sonnet" in m:
        return "sonnet"
    if "haiku" in m:
        return "haiku"
    return None


def spend_usd(key, inp, out, cache_read, cache_create):
    p = MODELS[key]
    return (
        inp * p["in"]
        + out * p["out"]
        + cache_read * p["in"] * CACHE_READ_MULT
        + cache_create * p["in"] * CACHE_WRITE_MULT
    ) / 1_000_000.0
