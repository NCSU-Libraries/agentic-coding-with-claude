# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Materials for **Data Science Special Topics: Agentic Coding with Claude**, an NC State University Libraries Data
Science Services workshop taught by Alp Tezbasaran.

- **When:** Thursday 2026-10-15, 2:00–3:30 pm.
- **Where: in person** in South Learning Lab 3430, D. H. Hill Jr. Library. The event page wrongly says "online".
- **Event page:** https://www.lib.ncsu.edu/workshops/data-science-special-topics-agentic-coding-claude/2026-10-15
- **Contacts:** workshop questions go to lib-datascienceservices@ncsu.edu. Access and setup help goes to
  go.ncsu.edu/getdatahelp.

The event description is the starting point, not a contract. Alp's priority is how good the session is for the
people in the room.

**Design (agreed 2026-10-15):** one shared task that everyone works on, a messy spreadsheet → a one-page dashboard.
It runs through eight steps: read, plan, act, check, remember, skill, undo, share. The last ten minutes are "make it
yours". There are two interchangeable activities, study-room bookings and a campus café. One runs live and the
other is self-guided. Which one runs live is set in `site/_variables.yml` (`live`, `self-guided`). The comparison is in
`instructor/decision-memo.md`.

## Layout

| Path | Contents |
| --- | --- |
| `site/` | Quarto website plus two reveal.js decks (`site/slides/<activity>.qmd`) |
| `site/slides/_*.qmd` | Slides shared by both decks, pulled in with `{{< include >}}` |
| `starters/<activity>/` | What attendees download: `README.md` plus one CSV. Nothing else |
| `examples/<activity>/` | The finished folder from a rehearsal run |
| `instructor/` | Facilitation guide, decision memo, answer keys, rehearsal transcripts, registrant email |
| `tools/make_data.py` | Seeded generator for both CSVs and `instructor/answer-keys.json` |
| `tools/package.sh` | Builds `site/downloads/*.zip` and `site/examples/` (both gitignored) |
| `tools/shoot.mjs` | Headless Chrome screenshots of pages or slides. Gives a `slide` index in reading order |
| `tools/record-tour.mjs` | Records the captioned walkthrough video |
| `tools/check_links.py` | Checks every link and image in `site/_site` (`--web` also requests external URLs) |
| `tools/demo-folder.sh` | Makes a fresh demo folder outside the repo and clears its Claude Code memory |

## Commands

```bash
Q=/Applications/RStudio.app/Contents/Resources/app/quarto/bin/quarto   # Quarto isn't on PATH on this Mac
bash tools/package.sh && $Q render site                                  # full build into site/_site
$Q render site/slides/study-rooms.qmd                                    # one deck
uv run --with numpy --with pandas python tools/make_data.py              # regenerate data and answer keys
```

The Pages workflow (`.github/workflows/deploy-pages.yml`) runs `package.sh`, then `quarto render site` with Quarto
1.10.18. Only Alp pushes.

## Keeping things consistent

- **Every prompt appears in several places**: the activity page, the deck, the facilitation guide and the rehearsal
  transcripts. Change one, change them all. Attendees copy them word for word.
- **Answer keys come from `instructor/answer-keys.json`.** After regenerating the data, update the `key:` block in
  `site/_variables.yml`. Then update the numbers written out in the decks, the guide and the activity pages:
  - the `/goal` prompts;
  - the "what a wrong number tells you" tables.
- **Feature facts were checked against Claude Code 2.1.299 on 2026-10-14.** The list is under "Facts to have ready"
  in the facilitation guide. Re-check against https://code.claude.com/docs/llms.txt before changing any claim about
  Claude Code.
- Data is synthetic and the café and library are fictional. Keep it that way, so public share links can't pass for
  real Libraries numbers.

## Gotchas

- **Claude Code loads `CLAUDE.md` from every parent folder.** Never run a demo or rehearsal inside this repo: it
  would read this file and the instructor notes, and the hidden rule each activity depends on is in
  `instructor/facilitation-guide.md`. Demo folders live in `../agentic-coding-demo/`, outside the repo.
- **Starter folders must stay clean.** No `CLAUDE.md`, no notes, nothing that states the rule Claude is supposed to
  miss. `README.md` there is a plain data dictionary.
- **Nested Claude Code sessions are blocked** from inside a Claude Code session by the auto-mode classifier. The
  rehearsals in `instructor/rehearsals/` are Sonnet sub-agents told to act as Claude Code on a Mac without Python.
  A real CLI rehearsal is a manual step for Alp, described in the facilitation guide. Attendees run Opus 5.5, the
  default on every paid plan since 2.1.280, so Sonnet rehearsal results are only a guide.
- **Rehearse and present with a clean Claude Code profile** (`CLAUDE_CONFIG_DIR=~/.claude-demo`). Alp's own setup has
  plugins and settings attendees don't, and `tools/demo-folder.sh` clears memory in whichever profile is set.
- **Quarto slides:**
  - Quarto gives level-1 (`#`) section slides the class `title-slide`, and `ncsu.scss` paints that white. The
    `.divider` rules in `site/theme/slides.scss` keep them red.
  - Slides nest under `#` sections, so `Reveal.slide(n)` doesn't step through them in order. `shoot.mjs` uses
    `Reveal.getSlides()` instead.
- **The zips have no enclosing folder.** That way both macOS Archive Utility and Windows "Extract All" produce exactly
  one `study-rooms/` or `cafe/` folder.
- `instructor/` names each activity's trap. The site never links to it. Decide before making the repo public.
