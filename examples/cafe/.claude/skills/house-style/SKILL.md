---
name: house-style
description: 'Gives any web page the NC State look: Wolfpack Red (#CC0000) highlights, dark gray text on white, Arial or Helvetica, a red header bar with the page title, and a footer that says "Synthetic data made for a workshop." Use whenever you create or restyle a web page, HTML file, dashboard or flyer.'
---

# House style: the NC State look

Apply this whenever you create or restyle a web page. If you were given a file name as an argument, restyle that file and keep its content and behavior unchanged. Otherwise apply the style to the page you are creating.

## The rules

| Part | Rule |
| --- | --- |
| Highlight color | Wolfpack Red `#CC0000`, for highlights only (see "Using red well") |
| Text and background | Dark gray text `#333333` on a white `#FFFFFF` page. Secondary text `#666666` |
| Font | `Arial, Helvetica, sans-serif` everywhere, including buttons, tables and chart labels |
| Header | A full-width red `#CC0000` bar at the top holding the page title in white |
| Footer | A footer at the bottom that says exactly: Synthetic data made for a workshop. |

## Using red well

- Red is for highlights: the header bar, a selected button, a thin rule under headings, and the one thing in a chart or table the reader should notice. If everything is red, nothing stands out.
- In charts, draw the thing to notice in red and the rest in grays (`#B3B3B3`, `#8C8C8C`, `#E3E3E3`). A light red tint (`rgba(204, 0, 0, 0.10)`) works for highlighted bands.
- Keep the page white. Separate sections with thin light-gray lines (`#D9D9D9`), not colored boxes.
- White text on `#CC0000` is fine. Never put gray text on red, and keep body text dark gray rather than red or pure black.
- Do not rely on color alone: add labels, signs or outlines too.

## Starter CSS and markup

```html
<style>
  :root { --red: #CC0000; --ink: #333333; --muted: #666666; --line: #D9D9D9; }
  body { margin: 0; background: #fff; color: var(--ink); font: 16px/1.45 Arial, Helvetica, sans-serif; }
  .wrap { max-width: 1120px; margin: 0 auto; padding: 0 16px; }
  .site-header { background: var(--red); color: #fff; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  .site-header h1 { margin: 0; padding: 16px 0; font-size: 1.6rem; line-height: 1.2; }
  .site-footer { border-top: 3px solid var(--red); margin-top: 24px; padding: 16px 0; color: var(--muted); font-size: .9rem; }
</style>

<header class="site-header"><div class="wrap"><h1>Page title here</h1></div></header>
<main class="wrap"> ... </main>
<footer class="site-footer"><div class="wrap">Synthetic data made for a workshop.</div></footer>
```

## Checklist before you finish

- [ ] The header bar is `#CC0000` and shows the page title in white.
- [ ] The footer text is exactly: Synthetic data made for a workshop.
- [ ] Text is dark gray on white and the font is Arial or Helvetica.
- [ ] Red is used for highlights only.
- [ ] Single-file pages keep their CSS in a `<style>` block and load nothing from the internet.
