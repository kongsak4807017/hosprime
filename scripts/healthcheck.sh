#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE_INPUT="${HOSPRIME_ENV_FILE:-$ROOT_DIR/.env}"
PROJECT_NAME="${HOSPRIME_COMPOSE_PROJECT_NAME:-hosprime}"
EXPECTED_GIT_SHA="${HOSPRIME_EXPECTED_GIT_SHA:-}"
HTTP_CONNECT_TIMEOUT_SECONDS="${HOSPRIME_HTTP_CONNECT_TIMEOUT_SECONDS:-5}"
HTTP_MAX_TIME_SECONDS="${HOSPRIME_HTTP_MAX_TIME_SECONDS:-15}"

fail() { printf 'ERROR: %s\n' "$*" >&2; exit 1; }
require() { command -v "$1" >/dev/null 2>&1 || fail "Required command not found: $1"; }
validate_port() {
  local key="$1" value="$2"
  [[ "$value" =~ ^[0-9]+$ ]] || fail "$key must be an integer between 1 and 65535"
  (( 10#$value >= 1 && 10#$value <= 65535 )) || fail "$key must be between 1 and 65535"
}
published_port() {
  local service="$1" container_port="$2" bindings port
  bindings="$(
    compose port "$service" "$container_port" \
      | tr -d '\r' \
      | awk 'NF' \
      | sort -u
  )"
  [[ -n "$bindings" ]] || fail "No published host port for $service:$container_port in Compose project $PROJECT_NAME"
  [[ "$bindings" != *$'\n'* ]] || fail "Multiple published host ports for $service:$container_port in Compose project $PROJECT_NAME"
  [[ "$bindings" =~ ^127\.0\.0\.1:([0-9]+)$ ]] || fail "Published binding must use 127.0.0.1 for $service:$container_port in Compose project $PROJECT_NAME"
  port="${BASH_REMATCH[1]}"
  validate_port "${service^^}_PUBLISHED_PORT" "$port"
  printf '%s' "$port"
}
container_id() {
  local service="$1" ids
  ids="$(compose ps -q "$service" | tr -d '\r' | awk 'NF' | sort -u)"
  [[ -n "$ids" ]] || fail "Service container does not exist in Compose project $PROJECT_NAME: $service"
  [[ "$ids" != *$'\n'* ]] || fail "Expected exactly one container for service $service in Compose project $PROJECT_NAME"
  [[ "$ids" =~ ^[0-9a-f]{12,64}$ ]] || fail "Unexpected container identifier for service $service"
  printf '%s' "$ids"
}
container_state() {
  docker inspect --format '{{.State.Status}}' "$1"
}
container_health() {
  docker inspect --format '{{if .State.Health}}{{.State.Health.Status}}{{else}}none{{end}}' "$1"
}
container_compose_identity() {
  docker inspect --format '{{ index .Config.Labels "com.docker.compose.project" }}|{{ index .Config.Labels "com.docker.compose.service" }}' "$1"
}
container_image_id() {
  local image_id
  image_id="$(docker inspect --format '{{.Image}}' "$1")" || fail "Unable to inspect image identity for container $1"
  [[ "$image_id" =~ ^sha256:[0-9a-f]{64}$ ]] || fail "Unexpected image identity for container $1"
  printf '%s' "$image_id"
}
image_source_revision() {
  local image_id="$1" revision
  revision="$(docker image inspect --format '{{ index .Config.Labels "org.opencontainers.image.revision" }}' "$image_id")" || fail "Unable to inspect source revision for image $image_id"
  [[ "$revision" =~ ^[0-9a-f]{40}$ ]] || fail "Application image is missing a valid source revision label"
  printf '%s' "$revision"
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
[[ -z "$EXPECTED_GIT_SHA" || "$EXPECTED_GIT_SHA" =~ ^[0-9a-f]{40}$ ]] || fail "HOSPRIME_EXPECTED_GIT_SHA must be a full lowercase commit SHA"
require docker
require curl
require python3
require awk
require git
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

TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

cd "$ROOT_DIR"
SOURCE_SHA="$(git rev-parse --verify HEAD 2>/dev/null)" || fail "HosPrime source must be a Git checkout"
[[ "$SOURCE_SHA" =~ ^[0-9a-f]{40}$ ]] || fail "Unable to resolve an exact HosPrime source commit"
[[ -z "$(git status --porcelain=v1 --untracked-files=all)" ]] || fail "HosPrime checkout must be pristine for health evidence"
[[ -z "$EXPECTED_GIT_SHA" || "$SOURCE_SHA" == "$EXPECTED_GIT_SHA" ]] || fail "HosPrime source commit changed between bootstrap and health verification"
export HOSPRIME_BUILD_GIT_SHA="$SOURCE_SHA"
compose config --quiet

for service in postgres redis neo4j backend frontend; do
  cid="$(container_id "$service")"
  identity="$(container_compose_identity "$cid")"
  [[ "$identity" == "$PROJECT_NAME|$service" ]] || fail "Container identity mismatch for service $service in Compose project $PROJECT_NAME"
  state="$(container_state "$cid")"
  [[ "$state" == "running" ]] || fail "Service is not running: $service ($state)"
  health="$(container_health "$cid")"
  [[ "$health" == "healthy" ]] || fail "Service is not healthy: $service ($health)"
  if [[ "$service" == "backend" || "$service" == "frontend" ]]; then
    image_id="$(container_image_id "$cid")"
    revision="$(image_source_revision "$image_id")"
    [[ "$revision" == "$SOURCE_SHA" ]] || fail "Application image source revision mismatch for service $service"
  fi
done

POSTGRES_PORT="$(published_port postgres 5432)"
REDIS_PORT="$(published_port redis 6379)"
NEO4J_HTTP_PORT="$(published_port neo4j 7474)"
NEO4J_BOLT_PORT="$(published_port neo4j 7687)"
BACKEND_PORT="$(published_port backend 8000)"
FRONTEND_PORT="$(published_port frontend 80)"
BACKEND_URL="http://127.0.0.1:${BACKEND_PORT}"
FRONTEND_URL="http://127.0.0.1:${FRONTEND_PORT}"

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

printf 'HosPrime health check passed (Compose project: %s, source commit: %s).\n' "$PROJECT_NAME" "$SOURCE_SHA"
printf 'Verified loopback bindings: postgres=%s redis=%s neo4j-http=%s neo4j-bolt=%s backend=%s frontend=%s\n' \
  "$POSTGRES_PORT" "$REDIS_PORT" "$NEO4J_HTTP_PORT" "$NEO4J_BOLT_PORT" "$BACKEND_PORT" "$FRONTEND_PORT"
printf 'Backend: %s\nFrontend: %s\n' "$BACKEND_URL" "$FRONTEND_URL"
compose ps
