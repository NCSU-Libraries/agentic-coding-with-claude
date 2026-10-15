#!/usr/bin/env bash
# Sets up, or resets, a fresh demo folder for the live session or a rehearsal, outside this repo.
#
#   bash tools/demo-folder.sh study-rooms     # or: cafe
#
# Creates ../agentic-coding-demo/<activity>/, next to this repo, from starters/<activity>/, and empties
# Claude Code's auto memory for that folder, so the session doesn't remember a rehearsal. The folder sits outside
# the repo on purpose: Claude Code reads CLAUDE.md from every parent folder, and this repo's notes name the trap.
# Presenting with a separate Claude Code profile? Export CLAUDE_CONFIG_DIR first; the memory is cleared there.
set -euo pipefail
activity=${1:?usage: bash tools/demo-folder.sh study-rooms|cafe}
case "$activity" in study-rooms|cafe) ;; *) echo "usage: bash tools/demo-folder.sh study-rooms|cafe"; exit 1 ;; esac
repo=$(cd "$(dirname "$0")/.." && pwd)
src="$repo/starters/$activity"

demo_root="$(dirname "$repo")/agentic-coding-demo"
dest="$demo_root/$activity"
mkdir -p "$demo_root"
rm -rf "$dest"
mkdir -p "$dest"
cp "$src"/* "$dest"/

# Claude Code keeps auto memory per project folder, in its profile folder (CLAUDE_CONFIG_DIR, or ~/.claude), under a
# name made from the path with every character other than a letter or digit turned into "-".
# Only the memory/ folder is removed; past session transcripts stay, and a fresh `claude` doesn't read them.
memory="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/projects/$(echo "$dest" | sed 's#[^A-Za-z0-9]#-#g')/memory"
rm -rf "$memory"

echo "Fresh demo folder: $dest"
echo "Cleared Claude Code memory for it: $memory"
echo
echo "Next:  cd \"$dest\" && claude"
echo "Prompts, in order: instructor/prompts-$activity.txt"
