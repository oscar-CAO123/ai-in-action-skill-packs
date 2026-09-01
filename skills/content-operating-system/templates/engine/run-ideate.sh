#!/usr/bin/env bash
# Cron 2. Same resolution rules as run-ingest.sh.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$HERE/.." && pwd)"
cd "$ROOT"

mkdir -p outputs/logs

PY="${COS_PYTHON:-}"
if [ -z "$PY" ]; then
  if   [ -x "$ROOT/engine/.venv/bin/python" ]; then PY="$ROOT/engine/.venv/bin/python"
  elif [ -x /opt/homebrew/bin/python3 ];        then PY=/opt/homebrew/bin/python3
  elif [ -x /usr/local/bin/python3 ];           then PY=/usr/local/bin/python3
  else PY=/usr/bin/python3
  fi
fi

echo "=== ideate $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
echo "python: $PY"
cd "$ROOT/engine" && exec "$PY" -m cos.ideate "$@"
