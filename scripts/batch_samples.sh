#!/usr/bin/env bash
# EP-002 — batch solve sample CSV / .bcproj without Studio/Qt.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="${1:-$ROOT/out/batch-samples}"
cd "$ROOT"
mkdir -p "$OUT"
python -m boardcomposer.batch_cli \
  --input "$ROOT/data/samples/batch_inbox" \
  --output "$OUT" \
  --profile "$ROOT/data/samples/batch_profile.json"
echo "Wrote $OUT/manifest.json"
