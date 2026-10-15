# Campus café sales

Synthetic daily sales for a fictional campus café, Aug 18, 2025 to May 8, 2026, made for an NC State University Libraries workshop. Files: `cafe_sales.csv` (the data), `README.md` (what each column means), `dashboard.html` (a one-page dashboard).

## What we learned about the data

- **Exam weeks** are not in the data. The café manager gave these dates:
  - Fall 2025: Oct 6–10 and Dec 8–16
  - Spring 2026: Mar 2–6 and Apr 28–May 7

  In `dashboard.html` they live in the `EXAM_WEEKS` list near the top of the script. Keep the two in sync.
- **Closed days:** a day on which every item has `units_sold` of 0 means the café was closed, not that it sold nothing. Leave closed days out of averages and show them as gaps.
- **Cold Brew:** `Cold Brew Coffee` is the same item as `Cold Brew` (it appears under the new name from 2026-01-07). Count them as one item.
