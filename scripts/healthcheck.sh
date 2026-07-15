#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="${HOSPRIME_ENV_FILE:-$ROOT_DIR/.env}"

fail() { printf 'ERROR: %s\n' "$*" >&2; exit 1; }
require() { command -v "$1" >/dev/null 2>&1 || fail "Required command not found: $1"; }
read_env() {
  local key="$1" default_value="$2" value
  value="$(grep -E "^[[:space:]]*${key}=" "$ENV_FILE" | tail -n 1 | cut -d= -f2- | tr -d '\r' || true)"
  printf '%s' "${value:-$default_value}"
}

require docker
require curl
require python3
[[ -f "$ENV_FILE" ]] || fail "Environment file not found: $ENV_FILE"
docker compose version >/dev/null 2>&1 || fail "Docker Compose v2 is required"

BACKEND_PORT="$(read_env BACKEND_PORT 8000)"
FRONTEND_PORT="$(read_env FRONTEND_PORT 80)"
BACKEND_URL="http://127.0.0.1:${BACKEND_PORT}"
FRONTEND_URL="http://127.0.0.1:${FRONTEND_PORT}"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

cd "$ROOT_DIR"
docker compose --env-file "$ENV_FILE" config --quiet

docker compose --env-file "$ENV_FILE" ps --status running --services > "$TMP_DIR/running-services.txt"
for service in postgres redis neo4j backend frontend; do
  grep -Fxq "$service" "$TMP_DIR/running-services.txt" || fail "Service is not running: $service"
done

curl --fail --silent --show-error "$BACKEND_URL/health/live" > "$TMP_DIR/live.json"
curl --fail --silent --show-error "$BACKEND_URL/health/ready" > "$TMP_DIR/ready.json"
curl --fail --silent --show-error "$FRONTEND_URL/" > "$TMP_DIR/frontend.html"
[[ -s "$TMP_DIR/frontend.html" ]] || fail "Frontend returned an empty response"

python3 - "$TMP_DIR/live.json" "$TMP_DIR/ready.json" <<'PY'
import json
import sys
from pathlib import Path

live = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
ready = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
if live.get("status") != "live":
    raise SystemExit(f"Unexpected liveness response: {live}")
if ready.get("status") not in {"ready", "degraded"}:
    raise SystemExit(f"Unexpected readiness response: {ready}")
if ready.get("database_dialect") != "postgresql":
    raise SystemExit(f"Expected PostgreSQL runtime: {ready}")
PY

printf 'HosPrime health check passed.\n'
printf 'Backend: %s\nFrontend: %s\n' "$BACKEND_URL" "$FRONTEND_URL"
docker compose --env-file "$ENV_FILE" ps
