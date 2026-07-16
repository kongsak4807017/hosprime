#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="${HOSPRIME_ENV_FILE:-$ROOT_DIR/.env}"
SKIP_BUILD=false

for arg in "$@"; do
  case "$arg" in
    --skip-build) SKIP_BUILD=true ;;
    -h|--help)
      cat <<'EOF'
Usage: scripts/bootstrap.sh [--skip-build]

Creates .env from .env.example when missing, validates configuration,
builds and starts HosPrime, then runs the health check.
EOF
      exit 0
      ;;
    *) printf 'Unknown argument: %s\n' "$arg" >&2; exit 2 ;;
  esac
done

fail() { printf 'ERROR: %s\n' "$*" >&2; exit 1; }
require() { command -v "$1" >/dev/null 2>&1 || fail "Required command not found: $1"; }

require docker
require curl
require python3
docker info >/dev/null 2>&1 || fail "Docker daemon is not available"
docker compose version >/dev/null 2>&1 || fail "Docker Compose v2 is required"

cd "$ROOT_DIR"
if [[ ! -f "$ENV_FILE" ]]; then
  cp .env.example "$ENV_FILE"
  chmod 600 "$ENV_FILE" 2>/dev/null || true
  printf 'Created %s from .env.example. Replace every CHANGE_ME value, then run this command again.\n' "$ENV_FILE"
  exit 2
fi

if awk '!/^[[:space:]]*(#|$)/ && /CHANGE_ME/ { found = 1 } END { exit(found ? 0 : 1) }' "$ENV_FILE"; then
  fail "$ENV_FILE still contains CHANGE_ME placeholders"
fi

docker compose --env-file "$ENV_FILE" config --quiet
if [[ "$SKIP_BUILD" == false ]]; then
  docker compose --env-file "$ENV_FILE" build
fi
docker compose --env-file "$ENV_FILE" up --detach --wait --wait-timeout 240
HOSPRIME_ENV_FILE="$ENV_FILE" "$ROOT_DIR/scripts/healthcheck.sh"

printf 'HosPrime local stack is ready.\n'