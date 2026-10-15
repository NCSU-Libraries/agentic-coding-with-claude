---
name: house-style
description: "Use whenever you create or restyle a web page (HTML, CSS, dashboard, report or summary page). Gives it the NC State look: Wolfpack Red #CC0000 for highlights, dark gray text on white, Arial or Helvetica, a red header bar with the page title, and a footer that says 'Synthetic data made for a workshop.'"
---

# House style: the NC State look

Apply these rules to every web page we make or restyle.

Target: $ARGUMENTS (if that is empty, apply the rules to the page you are creating or editing).

## Rules

1. **Highlight color is Wolfpack Red `#CC0000`.** Use it for highlights only: the header bar, key numbers, highlighted chart bars, active buttons, links and thin accent rules. Everything else is gray, black or white. No other accent colors.
2. **Text is dark gray on white.** Page background `#FFFFFF`, body text `#333333`, secondary text no lighter than `#666666`. Panels are white with a `#D9D9D9` border.
3. **Font is Arial or Helvetica.** Use `font-family: Arial, Helvetica, sans-serif`. No web fonts and no external requests.
4. **Header is a full-width red bar** (`#CC0000`) holding the page title as the `<h1>`, in white. The `<title>` tag and the `<h1>` say the same thing.
5. **Footer says exactly** `Synthetic data made for a workshop.` (with the final period) at the bottom of every page.

## Starter

```html
<style>
  :root { --red: #CC0000; --ink: #333333; --muted: #666666; --line: #D9D9D9; }
  body { margin: 0; background: #FFFFFF; color: var(--ink); font-family: Arial, Helvetica, sans-serif; line-height: 1.45; }
  .inner { max-width: 1120px; margin: 0 auto; padding: 0 16px; }
  .site-header { background: var(--red); color: #FFFFFF; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  .site-header h1 { margin: 0; padding: 16px 0; font-size: 1.6rem; }
  .site-footer { margin-top: 32px; border-top: 3px solid var(--red); color: var(--muted); font-size: 0.9rem; }
  .site-footer .inner { padding-top: 14px; padding-bottom: 14px; }
</style>

<header class="site-header"><div class="inner"><h1>PAGE TITLE</h1></div></header>
<main class="inner"> ...page content... </main>
<footer class="site-footer"><div class="inner">Synthetic data made for a workshop.</div></footer>
```

## When restyling an existing page

Keep the content, scripts and data exactly as they are. Change only colors, fonts, the header and the footer. For charts, use red for the highlighted series and grays for the rest, and keep value labels and legends so color is never the only cue.

## Before you finish

- The red header bar, the footer sentence and the Arial/Helvetica font are all present.
- No colors, fonts or footer wording are left over from the old style (search the file for them).
- Text contrast stays at or above 4.5:1. White on `#CC0000` is 5.9:1 and `#333333` on white is 12.6:1.
