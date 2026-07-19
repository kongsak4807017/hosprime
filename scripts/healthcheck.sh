#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE_INPUT="${HOSPRIME_ENV_FILE:-$ROOT_DIR/.env}"
PROJECT_NAME="${HOSPRIME_COMPOSE_PROJECT_NAME:-hosprime}"
HTTP_CONNECT_TIMEOUT_SECONDS="${HOSPRIME_HTTP_CONNECT_TIMEOUT_SECONDS:-5}"
HTTP_MAX_TIME_SECONDS="${HOSPRIME_HTTP_MAX_TIME_SECONDS:-15}"

fail() { printf 'ERROR: %s\n' "$*" >&2; exit 1; }
require() { command -v "$1" >/dev/null 2>&1 || fail "Required command not found: $1"; }
read_env() {
  local key="$1" default_value="$2" value
  value="$(grep -E "^[[:space:]]*${key}=" "$ENV_FILE" | tail -n 1 | cut -d= -f2- | tr -d '\r' | xargs || true)"
  printf '%s' "${value:-$default_value}"
}
validate_port() {
  local key="$1" value="$2"
  [[ "$value" =~ ^[0-9]+$ ]] || fail "$key must be an integer between 1 and 65535"
  (( value >= 1 && value <= 65535 )) || fail "$key must be between 1 and 65535"
}
container_id() {
  compose ps -q "$1"
}
container_state() {
  docker inspect --format '{{.State.Status}}' "$1"
}
container_health() {
  docker inspect --format '{{if .State.Health}}{{.State.Health.Status}}{{else}}none{{end}}' "$1"
}
http_get() {
  curl \
    --fail \
    --silent \
    --show-error \
    --connect-timeout "$HTTP_CONNECT_TIMEOUT_SECONDS" \
    --max-time "$HTTP_MAX_TIME_SECONDS" \
    "$1"
}

[[ "$PROJECT_NAME" =~ ^[a-z0-9][a-z0-9_-]*$ ]] || fail "HOSPRIME_COMPOSE_PROJECT_NAME must match ^[a-z0-9][a-z0-9_-]*$"
require docker
require curl
require python3
ENV_FILE="$(python3 - "$ENV_FILE_INPUT" <<'PY'
import os
import sys
print(os.path.abspath(sys.argv[1]))
PY
)"
compose() { docker compose --project-name "$PROJECT_NAME" --env-file "$ENV_FILE" "$@"; }
[[ -f "$ENV_FILE" ]] || fail "Environment path is not a regular file: $ENV_FILE"
[[ ! -L "$ENV_FILE" ]] || fail "Environment file must not be a symbolic link: $ENV_FILE"
docker compose version >/dev/null 2>&1 || fail "Docker Compose v2 is required"

BACKEND_PORT="$(read_env BACKEND_PORT 8000)"
FRONTEND_PORT="$(read_env FRONTEND_PORT 80)"
validate_port BACKEND_PORT "$BACKEND_PORT"
validate_port FRONTEND_PORT "$FRONTEND_PORT"
BACKEND_URL="http://127.0.0.1:${BACKEND_PORT}"
FRONTEND_URL="http://127.0.0.1:${FRONTEND_PORT}"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

cd "$ROOT_DIR"
compose config --quiet

for service in postgres redis neo4j backend frontend; do
  cid="$(container_id "$service")"
  [[ -n "$cid" ]] || fail "Service container does not exist in Compose project $PROJECT_NAME: $service"
  state="$(container_state "$cid")"
  [[ "$state" == "running" ]] || fail "Service is not running: $service ($state)"
  health="$(container_health "$cid")"
  [[ "$health" == "healthy" ]] || fail "Service is not healthy: $service ($health)"
done

http_get "$BACKEND_URL/health/live" > "$TMP_DIR/live.json"
http_get "$BACKEND_URL/health/ready" > "$TMP_DIR/ready.json"
http_get "$FRONTEND_URL/" > "$TMP_DIR/frontend.html"
[[ -s "$TMP_DIR/frontend.html" ]] || fail "Frontend returned an empty response"

python3 - "$TMP_DIR/live.json" "$TMP_DIR/ready.json" <<'PY'
import json
import sys
from pathlib import Path

live = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
ready = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
if live.get("status") != "live":
    raise SystemExit(f"Unexpected liveness response: {live}")
if ready.get("status") != "ready":
    raise SystemExit(f"Backend is not fully ready: {ready}")
if ready.get("database_dialect") != "postgresql":
    raise SystemExit(f"Expected PostgreSQL runtime: {ready}")
PY

printf 'HosPrime health check passed (Compose project: %s).\n' "$PROJECT_NAME"
printf 'Backend: %s\nFrontend: %s\n' "$BACKEND_URL" "$FRONTEND_URL"
compose ps
