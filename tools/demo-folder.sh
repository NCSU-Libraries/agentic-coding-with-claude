#!/usr/bin/env bash
# Sets up, or resets, a fresh demo folder for the live session or a rehearsal, outside this repo.
#
#   bash tools/demo-folder.sh study-rooms     # or: cafe
#
# Creates ~/Desktop/projects/dss/workshops/agentic-coding-demo/<activity>/ from starters/<activity>/, and deletes
# Claude Code's auto memory for that folder, so the session doesn't remember a rehearsal. The folder sits outside
# the repo on purpose: Claude Code reads CLAUDE.md from every parent folder, and this repo's notes name the trap.
set -euo pipefail
activity=${1:?usage: bash tools/demo-folder.sh study-rooms|cafe}
repo=$(cd "$(dirname "$0")/.." && pwd)
src="$repo/starters/$activity"
[ -d "$src" ] || { echo "No starter called $activity"; exit 1; }

demo_root="$HOME/Desktop/projects/dss/workshops/agentic-coding-demo"
dest="$demo_root/$activity"
mkdir -p "$demo_root"
rm -rf "$dest"
mkdir -p "$dest"
cp "$src"/* "$dest"/

# Claude Code keeps auto memory per project folder, under a name made from the path with "/" turned into "-".
memory="$HOME/.claude/projects/$(echo "$dest" | sed 's#/#-#g')"
rm -rf "$memory"

echo "Fresh demo folder: $dest"
echo "Cleared Claude Code memory for it: $memory"
echo
echo "Next:  cd \"$dest\" && claude"
echo "Prompts, in order: instructor/prompts-$activity.txt"
