# Campus café sales

Daily sales from a campus café's register, from the first day of fall classes (August 18, 2025) through May 8, 2026.

**This data is synthetic.** It was made up for the NC State University Libraries workshop *Agentic Coding with
Claude*. The café, its menu and its sales are fictional; don't read anything into the numbers.

## Files

| File | What it is |
| --- | --- |
| `cafe_sales.csv` | One row per menu item per day |

## Columns

| Column | Meaning | Example |
| --- | --- | --- |
| `date` | Day, `YYYY-MM-DD` | `2025-08-18` |
| `item` | Menu item | `Latte` |
| `category` | `Coffee`, `Tea`, `Other drinks`, `Bakery`, or `Food` | `Coffee` |
| `units_sold` | How many were sold that day | `69` |
| `unit_price` | Price of one, in dollars | `4.50` |
| `high_temp_f` | That day's high temperature on campus, °F | `83` |

## Background

- The café is open seven days a week, with shorter hours on weekends.
- Some prices went up when the spring semester started in January 2026.
- A new register was installed over winter break.
