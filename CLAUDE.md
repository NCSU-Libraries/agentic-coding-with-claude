# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Materials for **Data Science Special Topics: Agentic Coding with Claude**, an NC State University Libraries Data
Science Services (DSS) workshop taught by Alp Tezbasaran. It runs **Thursday 2026-10-15, 2:00–3:30pm**. The event
page (https://www.lib.ncsu.edu/workshops/data-science-special-topics-agentic-coding-claude/2026-10-15) lists a room
(South Learning Lab 3430, D. H. Hill Jr. Library). The description and the drafted catalog note both say the session
is **online** (Zoom), so plan for screen-share. Confirm the format with Alp before writing logistics into anything
attendee-facing.

As of 2026-10-14 the folder is empty and not a git repository. There is no build, lint or test tooling yet.

## What the event page promises

Judge every draft against this list, not against the older plan described below.

- What an AI agent is, and how it differs from a chatbot.
- **Installing Claude Code together.**
- Slash commands and the key features: project memory (`CLAUDE.md`), custom commands and skills.
- A small live task that shows the read → plan → act → verify loop, including common failures and how to catch
  them.
- Responsible-use habits.

Access constraints:

- Following along requires the attendee's own Claude account, set up beforehand. There is no campus-wide license,
  and accounts can't be created during the session. Attendees can also just watch. Exercises must work for people
  with no account.
- Contacts: workshop questions go to `lib-datascienceservices@ncsu.edu`. Access and setup help goes to
  `go.ncsu.edu/getdatahelp`. The two aren't interchangeable.

## Earlier material to build from (outside this folder)

All paths are under `~/Desktop/projects/dss/`.

- **`agentic-coding/claude/`**: the original plan, a git repo with two commits.
  - `facilitator-guide.md` has a 90-minute run-of-show: a messy synthetic CSV becomes a clean file, a chart and
    `findings.md`, with a live self-correction and a `git diff` check. It continues with memory (the centerpiece),
    slash commands, skills and a brief MCP segment. It includes two no-install pair exercises and cost/safety
    beats worked into the demo.
  - `README.md` has the five learning objectives.
  - `assets/` holds the Libraries logo and the MIT + CC-BY-4.0 license files.
  - The plan assumed an instructor-only demo with no installs. The event page now promises a shared install, and
    the agreed outline drops MCP. The guide and its objectives need a rewrite pass, not reuse as-is. Alp's notes on
    this are in the "Open" list under this session in `f26-workshops/drafted-descriptions.md`. They also flag that
    90 minutes is tight for install + features + a live task online.
  - The deeper should-we/ethics/landscape material belongs to a separate "AI Discussions" session.
- **`ise520-f26/`** and **`ise520-demo/`**: Claude Code was demoed live on the ER wait-time dataset on 2026-09-24.
  - These folders hold the exact prompts (`prompts/`), headless rehearsal transcripts (`rehearsals/`) and a finished
    fallback run.
  - The demo runbook is in `session-plan.md`.
  - `slides/` is a Quarto deck on the house theme.
- **`ai-workshops/`** (NCSU-Libraries/ai-workshops): the house repo layout (`workshops/<slug>/`, Quarto slides,
  GitHub Pages). It also holds *Colab and Chill*, the previous session in the series. That's where "AI as Knower"
  first came up; this session is the "Doer" follow-up.
- **`f26-workshops/drafted-descriptions.md`**: the catalog description drafted for this session, and its open
  items (public title, learning objectives, a confirmation email with the Zoom line).

## Conventions

- **Slides:** Quarto + reveal.js on the NCSU theme (`theme/ncsu.scss`, copy it from `ise520-f26/slides/theme/`). Use
  the footer "Data Science Services" and the Libraries logo.
  - Quarto is not on PATH on this Mac. Render with the Docker image used in ISE 520, run from the deck's parent
    folder: `docker run --rm -v "$PWD:/project" -w /project/slides slides-final:quarto quarto render index.qmd --to revealjs`.
  - RStudio's bundled binary also works: `/Applications/RStudio.app/Contents/Resources/app/quarto/bin/quarto`.
- **Python:** there's no project environment. `uv run --with pandas python <script>.py` works for ad-hoc scripts.
- **Licenses:** CC-BY-4.0 for content and MIT for code.
- **Audience:** any NC State affiliate. Keep everything beginner-friendly, and use synthetic data only, because
  that's what makes the data-governance point safe to demo.
- **Instructor-only files** (facilitator guide, run sheet) stay out of any public repo. Serve them as private
  Artifacts, as for Colab and Chill and ISE 520.

## Gotchas

- **Claude Code loads `CLAUDE.md` from every parent directory.** Any live demo project created under this folder
  would read this file, including the instructor notes and planned failures. Put demo folders outside this tree, as
  `ise520-demo/` sits beside `ise520-f26/`. Give each one its own git repo for `git diff` and resets
  (`git reset --hard && git clean -fd`), plus a finished fallback copy.
- If a `CLAUDE.md` is shown on screen as the memory example, use the demo project's file, not this one.
- **Check feature syntax against the current Claude Code docs before it goes on a slide or handout.** The old guide
  predates several changes. Check the `#` memory shortcut, `/init`, `/memory`, and whether custom commands
  (`.claude/commands/`) are still separate from skills (`.claude/skills/<name>/SKILL.md`). Also check `claude mcp
  add`, plan mode, and the current install command and account options.
