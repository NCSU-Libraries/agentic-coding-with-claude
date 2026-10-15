# Study-room bookings

An export of study-room reservations from a campus library's booking system, pulled on October 1, 2026. It runs from
the start of the spring 2024 semester through September 30, 2026.

**This data is synthetic.** It was made up for the NC State University Libraries workshop *Agentic Coding with
Claude*. The library, its rooms and its bookings are fictional; don't read anything into the numbers.

## Files

| File | What it is |
| --- | --- |
| `room_bookings.csv` | One row per booking |

## Columns

| Column | Meaning | Example |
| --- | --- | --- |
| `booking_id` | Unique ID the booking system gives each reservation | `SR-10001` |
| `date` | Day of the booking, `YYYY-MM-DD` | `2024-01-08` |
| `start_time` | Start time, 24-hour clock | `15:00` |
| `hours` | Length of the booking in hours | `1.5` |
| `room` | Room booked | `Room 203` |
| `group_size` | Number of people the person booking said would come. Sometimes left blank | `3` |
| `booked_by` | `Undergraduate`, `Graduate`, or `Faculty/Staff` | `Graduate` |

## Background

- Rooms 201–212 have been bookable the whole time. Rooms 204, 207 and 210 seat eight and have a large screen; the
  others seat four.
- Rooms 301–304 opened on the third floor in August 2025. They seat six.
- On weekends, rooms open at 11:00. The last booking of the day ends at midnight.
