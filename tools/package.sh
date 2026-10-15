#!/usr/bin/env bash
# Builds what the site serves from starters/ and examples/:
#   site/downloads/<name>.zip            each starter folder, for attendees
#   site/downloads/<name>-finished.zip   each finished example folder, for comparison and catching up
#   site/examples/<name>/                the finished example's pages, to view in the browser
#
#   bash tools/package.sh      (from the repo root; the Pages workflow runs it before rendering)
#
# The zips hold the files at their top level, with no enclosing folder: macOS's Archive Utility and
# Windows' "Extract All" then both make exactly one folder named after the zip.
set -euo pipefail
cd "$(dirname "$0")/.."

out=site/downloads
rm -rf "$out" site/examples
mkdir -p "$out" site/examples

for dir in starters/*/; do
  name=$(basename "$dir")
  (cd "$dir" && zip -q -X -r "../../$out/$name.zip" . -x '*.DS_Store')
done

for dir in examples/*/; do
  name=$(basename "$dir")
  if [ ! -f "$dir/dashboard.html" ]; then continue; fi
  (cd "$dir" && zip -q -X -r "../../$out/$name-finished.zip" . -x '*.DS_Store')
  mkdir -p "site/examples/$name"
  cp "$dir"/*.html "site/examples/$name/"
  # Show the memory and skill files as plain text pages next to the dashboards.
  if [ -f "$dir/CLAUDE.md" ]; then cp "$dir/CLAUDE.md" "site/examples/$name/CLAUDE.md.txt"; fi
  skill="$dir/.claude/skills/house-style/SKILL.md"
  if [ -f "$skill" ]; then cp "$skill" "site/examples/$name/SKILL.md.txt"; fi
done

ls -la "$out"
find site/examples -type f | sort
