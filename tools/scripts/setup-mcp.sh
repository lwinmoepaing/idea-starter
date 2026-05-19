#!/usr/bin/env bash
# Bootstrap project-scope MCP servers into .mcp-servers/.
# Run once after cloning. Re-run to update.
set -euo pipefail

cd "$(dirname "$0")/../.."
ROOT="$(pwd)"
SERVERS_DIR="$ROOT/.mcp-servers"
mkdir -p "$SERVERS_DIR"

# tldraw-render-mcp — not on npm, install from source.
# Requires: git, node, npm, bun (build uses bun). Postinstall downloads Chromium via Playwright (~150MB).
TLDRAW_DIR="$SERVERS_DIR/tldraw-render-mcp"
TLDRAW_REPO="https://github.com/bassimeledath/tldraw-render-mcp.git"

if [ -d "$TLDRAW_DIR/.git" ]; then
  echo "→ Updating tldraw-render-mcp"
  git -C "$TLDRAW_DIR" pull --ff-only
else
  echo "→ Cloning tldraw-render-mcp"
  git clone "$TLDRAW_REPO" "$TLDRAW_DIR"
fi

cd "$TLDRAW_DIR"
echo "→ npm install"
npm install
echo "→ npm run build"
npm run build

echo "✓ tldraw MCP ready at $TLDRAW_DIR/dist/index.js"
echo "  Claude Code will pick it up from .mcp.json on next session."
