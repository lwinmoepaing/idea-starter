#!/usr/bin/env bash
# Reset the generated workspace: wipe everything inside mvp/, docs/, plans/,
# reports/, and workflow/ EXCEPT README.md and .gitignore files.
#
# Scaffold subfolders that carry their own README.md (plans/todo, plans/done,
# workflow/ideas, workflow/approach, workflow/marketing) are preserved; purely
# generated dirs (mvp/src, mvp/node_modules, reports/*-screens, …) are removed
# once empty.
#
# Fully-generated, untracked dirs with no scaffold README to keep (PURGE) are
# removed wholesale, folder and all.
#
# Usage:
#   tools/scripts/clean.sh            # delete
#   tools/scripts/clean.sh -n         # dry run — list what would be deleted
set -euo pipefail

cd "$(dirname "$0")/../.."
ROOT="$(pwd)"

# Keep README.md + .gitignore, prune generated content.
TARGETS=(mvp docs plans reports workflow)
# Remove entirely — gitignored MCP/tooling output, nothing tracked inside.
PURGE=(.playwright-mcp)

DRY_RUN=0
if [[ "${1:-}" == "-n" || "${1:-}" == "--dry-run" ]]; then
  DRY_RUN=1
  echo "DRY RUN — nothing will be deleted"
fi

for dir in "${TARGETS[@]}"; do
  [ -d "$ROOT/$dir" ] || { echo "→ skip $dir/ (missing)"; continue; }

  if [ "$DRY_RUN" -eq 1 ]; then
    echo "=== $dir/ ==="
    # node_modules is removed wholesale — show it as a single line, not its
    # thousands of vendored files (which include their own README.md).
    find "$ROOT/$dir" -type d -name node_modules -prune -print
    find "$ROOT/$dir" -type d -name node_modules -prune -o \
      -type f ! -name 'README.md' ! -name '.gitignore' -print
    continue
  fi

  # 1. Drop vendored deps entirely (their package README.md would otherwise be
  #    kept by the rule below, leaving node_modules as surviving litter).
  find "$ROOT/$dir" -type d -name node_modules -prune -exec rm -rf {} +
  # 2. Delete every remaining file that isn't a README.md or .gitignore.
  find "$ROOT/$dir" -type f ! -name 'README.md' ! -name '.gitignore' -delete
  # 3. Remove directories left empty (bottom-up). Dirs still holding a README.md
  #    or .gitignore are not empty, so scaffold subfolders survive.
  find "$ROOT/$dir" -mindepth 1 -type d -empty -delete
  echo "✓ cleaned $dir/"
done

for dir in "${PURGE[@]}"; do
  [ -e "$ROOT/$dir" ] || { echo "→ skip $dir/ (missing)"; continue; }

  if [ "$DRY_RUN" -eq 1 ]; then
    echo "=== $dir/ (purge whole folder) ==="
    find "$ROOT/$dir" -print
    continue
  fi

  rm -rf "$ROOT/$dir"
  echo "✓ purged $dir/"
done

[ "$DRY_RUN" -eq 1 ] && echo "(dry run — re-run without -n to delete)" || echo "Done."
