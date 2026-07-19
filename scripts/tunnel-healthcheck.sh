#!/usr/bin/env bash
# tunnel-healthcheck.sh — verify Cloudflare tunnel is alive; self-heal if not.
# Added after 2026-07-09 incident: cloudflared container was missing entirely,
# sofia.synai.ai returned 530 while Access-protected routes masked the outage
# with edge 302s. Cron runs this every 5 minutes.

set -u
COMPOSE_DIR="/home/mello"
CHECK_URL="https://sofia.synai.ai/"
LOG_PREFIX="[$(date '+%Y-%m-%d %H:%M:%S')]"

log() { echo "$LOG_PREFIX $*"; }

# --- Check 1: container exists and is running -------------------------------
state=$(docker inspect cloudflared --format '{{.State.Status}}' 2>/dev/null || echo "missing")

# --- Check 2: route actually serves (200-399 = healthy; 302 alone is NOT
# proof of tunnel health since CF Access answers at the edge, but combined
# with a running container it's good enough) ---------------------------------
code=$(curl -s -o /dev/null -w '%{http_code}' --max-time 15 "$CHECK_URL" || echo "000")

if [ "$state" = "running" ] && [ "$code" -ge 200 ] && [ "$code" -lt 400 ] 2>/dev/null; then
    # Healthy — stay silent to keep the log signal-only.
    exit 0
fi

log "UNHEALTHY: cloudflared state=$state, $CHECK_URL returned $code — attempting recovery"

cd "$COMPOSE_DIR" || { log "FATAL: cannot cd to $COMPOSE_DIR"; exit 1; }
docker compose up -d cloudflared 2>&1 | tail -2 | while read -r line; do log "recover: $line"; done

# Give the tunnel time to register edge connections, then re-verify.
sleep 20
code2=$(curl -s -o /dev/null -w '%{http_code}' --max-time 15 "$CHECK_URL" || echo "000")
state2=$(docker inspect cloudflared --format '{{.State.Status}}' 2>/dev/null || echo "missing")

if [ "$state2" = "running" ] && [ "$code2" -ge 200 ] && [ "$code2" -lt 400 ] 2>/dev/null; then
    log "RECOVERED: cloudflared=$state2, $CHECK_URL returned $code2"
    exit 0
fi

log "STILL DOWN after recovery attempt: cloudflared=$state2, http=$code2 — manual intervention needed"
docker logs cloudflared --tail 5 2>&1 | while read -r line; do log "cloudflared: $line"; done
exit 1
