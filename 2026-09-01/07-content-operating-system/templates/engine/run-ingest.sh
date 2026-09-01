#!/usr/bin/env bash
# Cron 1. Called by the scheduler. Resolves its own paths, because a scheduler starts a job in
# a directory nobody chose and with a PATH that does not include what your shell has.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$HERE/.." && pwd)"
cd "$ROOT"

mkdir -p outputs/logs

# An absolute python. `python3: command not found` at 03:00 is the most common failure here.
PY="${COS_PYTHON:-}"
if [ -z "$PY" ]; then
  if   [ -x "$ROOT/engine/.venv/bin/python" ]; then PY="$ROOT/engine/.venv/bin/python"
  elif [ -x /opt/homebrew/bin/python3 ];        then PY=/opt/homebrew/bin/python3
  elif [ -x /usr/local/bin/python3 ];           then PY=/usr/local/bin/python3
  else PY=/usr/bin/python3
  fi
fi

echo "=== ingest $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
echo "python: $PY"
cd "$ROOT/engine" && exec "$PY" -m cos.ingest "$@"
