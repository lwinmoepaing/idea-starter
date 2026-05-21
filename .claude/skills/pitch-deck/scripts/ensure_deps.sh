#!/usr/bin/env bash
# Print the path to a Python interpreter that can `import reportlab`, installing
# it if needed. build_deck.py needs reportlab; this repo ships no venv and the
# system Python usually lacks it, so resolve a working interpreter once and let
# callers reuse it.
#
# Resolution order (cheapest first):
#   1. system python3 already has reportlab        -> use it
#   2. the skill-local venv already has reportlab   -> use it
#   3. create the skill-local venv + pip install    -> use it
#
# The venv lives inside the skill dir (.venv/, gitignored) so the skill stays
# self-contained and re-running is a no-op once it exists.
#
# Usage:  PYBIN="$(scripts/ensure_deps.sh)"  ||  exit 1
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
VENV="$SKILL_DIR/.venv"

# Everything diagnostic goes to stderr; stdout carries ONLY the interpreter path.
log() { echo "$@" >&2; }

has_reportlab() { "$1" -c "import reportlab" >/dev/null 2>&1; }

if has_reportlab python3; then
  command -v python3
  exit 0
fi

if [ -x "$VENV/bin/python" ] && has_reportlab "$VENV/bin/python"; then
  echo "$VENV/bin/python"
  exit 0
fi

log "→ reportlab not found; setting up $VENV"
python3 -m venv "$VENV" >&2
"$VENV/bin/pip" install --quiet --upgrade pip >&2
"$VENV/bin/pip" install --quiet reportlab >&2

if has_reportlab "$VENV/bin/python"; then
  echo "$VENV/bin/python"
  exit 0
fi

log "✗ could not make reportlab importable — install it manually (pip install reportlab)"
exit 1
