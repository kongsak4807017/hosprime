#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE_INPUT="${HOSPRIME_ENV_FILE:-$ROOT_DIR/.env}"
PROJECT_NAME="${HOSPRIME_COMPOSE_PROJECT_NAME:-hosprime}"
SKIP_BUILD=false

for arg in "$@"; do
  case "$arg" in
    --skip-build) SKIP_BUILD=true ;;
    -h|--help)
      cat <<'EOF'
Usage: scripts/bootstrap.sh [--skip-build]

Creates .env from .env.example when missing, validates configuration,
builds and starts HosPrime, then runs the health check.
Set HOSPRIME_ENV_FILE to an absolute path or a path relative to the caller.
Set HOSPRIME_COMPOSE_PROJECT_NAME to isolate this stack from other checkouts.
The checkout must be a pristine Git commit so runtime evidence is attributable.
Runtime environment files stored inside the repository must be ignored by Git.
Runtime environment files are restricted to the current user before Compose runs.
EOF
      exit 0
      ;;
    *) printf 'Unknown argument: %s\n' "$arg" >&2; exit 2 ;;
  esac
done

fail() { printf 'ERROR: %s\n' "$*" >&2; exit 1; }
require() { command -v "$1" >/dev/null 2>&1 || fail "Required command not found: $1"; }
assert_in_repo_env_is_ignored() {
  local relative_path
  if relative_path="$(python3 - "$ROOT_DIR" "$ENV_FILE" <<'PY'
import os
import sys

root = os.path.realpath(sys.argv[1])
path = os.path.realpath(sys.argv[2])
try:
    inside = os.path.commonpath((root, path)) == root
except ValueError:
    inside = False
if not inside:
    raise SystemExit(1)
print(os.path.relpath(path, root).replace(os.sep, "/"))
PY
  )"; then
    git check-ignore -q -- "$relative_path" || fail "Environment file inside repository must be ignored by Git: $relative_path"
  fi
}
protect_env_file() {
  chmod 600 "$ENV_FILE" || fail "Unable to restrict environment file permissions: $ENV_FILE"
  python3 - "$ENV_FILE" <<'PY' || fail "Environment file permissions must deny group and other access: $ENV_FILE"
import os
import stat
import sys

mode = stat.S_IMODE(os.stat(sys.argv[1], follow_symlinks=False).st_mode)
if mode & 0o077:
    raise SystemExit(1)
PY
}

[[ "$PROJECT_NAME" =~ ^[a-z0-9][a-z0-9_-]*$ ]] || fail "HOSPRIME_COMPOSE_PROJECT_NAME must match ^[a-z0-9][a-z0-9_-]*$"
require docker
require curl
require python3
require git
ENV_FILE="$(python3 - "$ENV_FILE_INPUT" <<'PY'
import os
import sys
print(os.path.abspath(sys.argv[1]))
PY
)"
compose() { docker compose --project-name "$PROJECT_NAME" --env-file "$ENV_FILE" "$@"; }

docker info >/dev/null 2>&1 || fail "Docker daemon is not available"
docker compose version >/dev/null 2>&1 || fail "Docker Compose v2 is required"

cd "$ROOT_DIR"
SOURCE_SHA="$(git rev-parse --verify HEAD 2>/dev/null)" || fail "HosPrime source must be a Git checkout"
[[ "$SOURCE_SHA" =~ ^[0-9a-f]{40}$ ]] || fail "Unable to resolve an exact HosPrime source commit"
[[ -z "$(git status --porcelain=v1 --untracked-files=all)" ]] || fail "HosPrime checkout must be pristine before bootstrap"
export HOSPRIME_BUILD_GIT_SHA="$SOURCE_SHA"

# Enforce the Git-ignore boundary before creating a new in-repository file.
# This prevents even the initial placeholder copy from becoming an untracked,
# credential-bearing file that can later be committed accidentally.
assert_in_repo_env_is_ignored

if [[ ! -e "$ENV_FILE" ]]; then
  [[ -d "$(dirname "$ENV_FILE")" ]] || fail "Environment file parent directory does not exist: $(dirname "$ENV_FILE")"
  cp .env.example "$ENV_FILE"
  chmod 600 "$ENV_FILE" || fail "Unable to restrict new environment file permissions: $ENV_FILE"
  printf 'Created %s from .env.example. Replace every CHANGE_ME value, then run this command again.\n' "$ENV_FILE"
  exit 2
fi
[[ -f "$ENV_FILE" ]] || fail "Environment path is not a regular file: $ENV_FILE"
[[ ! -L "$ENV_FILE" ]] || fail "Environment file must not be a symbolic link: $ENV_FILE"
protect_env_file

if awk '!/^[[:space:]]*(#|$)/ && /CHANGE_ME/ { found = 1 } END { exit(found ? 0 : 1) }' "$ENV_FILE"; then
  fail "$ENV_FILE still contains CHANGE_ME placeholders"
fi

compose config --quiet
if [[ "$SKIP_BUILD" == false ]]; then
  compose build
fi
compose up --detach --wait --wait-timeout 240
HOSPRIME_ENV_FILE="$ENV_FILE" HOSPRIME_COMPOSE_PROJECT_NAME="$PROJECT_NAME" HOSPRIME_EXPECTED_GIT_SHA="$SOURCE_SHA" HOSPRIME_BUILD_GIT_SHA="$SOURCE_SHA" bash "$ROOT_DIR/scripts/healthcheck.sh"

printf 'HosPrime local stack is ready (Compose project: %s, source commit: %s).\n' "$PROJECT_NAME" "$SOURCE_SHA"
