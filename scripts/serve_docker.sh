#!/usr/bin/env bash
# EP-003 SPR-003 — build & run the reference HTTP container.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
if [[ -z "${BOARDCOMPOSER_API_KEY:-}" ]]; then
  echo "warning: BOARDCOMPOSER_API_KEY unset — adapter will accept unauthenticated requests" >&2
fi
exec docker compose up --build "$@"
