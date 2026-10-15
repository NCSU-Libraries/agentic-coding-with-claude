"""Generate the two synthetic starter datasets and their answer keys.

    uv run --with numpy --with pandas python tools/make_data.py

Writes:
  starters/study-rooms/room_bookings.csv
  starters/cafe/cafe_sales.csv
  instructor/answer-keys.json   (copy the key numbers into site/_variables.yml, the decks and the guide)

Both datasets are made up. Each has one planted data problem that the answer key exposes:
  study-rooms: about 3.5% of bookings appear twice (an export glitch); booking_id should be unique.
  cafe:        one latte row has its price typed as 45.00 instead of 4.50.
Each also has smaller mess (old room labels, a renamed menu item, zero rows on closed days) and
one rule that lives only in the instructor's materials, never in the folder (see instructor/facilitation-guide.md).
Everything is seeded, so reruns produce identical files.
"""

from __future__ import annotations

import json
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
rng = np.random.default_rng(20261015)


def days(start: str, end: str) -> list[date]:
    d0, d1 = date.fromisoformat(start), date.fromisoformat(end)
    return [d0 + timedelta(n) for n in range((d1 - d0).days + 1)]


def in_any(d: date, ranges: list[tuple[str, str]]) -> bool:
    return any(date.fromisoformat(a) <= d <= date.fromisoformat(b) for a, b in ranges)


# ---------------------------------------------------------------------------------------------
# Study-room bookings: Jan 2024 to Sep 2026, one row per booking
# ---------------------------------------------------------------------------------------------

SEMESTERS = [
    ("2024-01-08", "2024-05-03"),
    ("2024-08-19", "2024-12-13"),
    ("2025-01-07", "2025-05-02"),
    ("2025-08-18", "2025-12-16"),
    ("2026-01-07", "2026-05-08"),
    ("2026-08-17", "2026-12-15"),
]
FINALS = [
    ("2024-04-25", "2024-05-03"),
    ("2024-12-05", "2024-12-13"),
    ("2025-04-24", "2025-05-02"),
    ("2025-12-08", "2025-12-16"),
    ("2026-04-28", "2026-05-08"),
]
MIDTERMS = [
    ("2024-02-26", "2024-03-01"),
    ("2024-10-07", "2024-10-11"),
    ("2025-03-03", "2025-03-07"),
    ("2025-10-06", "2025-10-10"),
    ("2026-03-02", "2026-03-06"),
]
SPRING_BREAKS = [("2024-03-04", "2024-03-08"), ("2025-03-10", "2025-03-14"), ("2026-03-09", "2026-03-13")]
THANKSGIVING = [("2024-11-27", "2024-11-29"), ("2025-11-26", "2025-11-28")]
FIRST_WEEKS = [(a, (date.fromisoformat(a) + timedelta(6)).isoformat()) for a, _ in SEMESTERS]
NEW_ROOMS_OPEN = date(2025, 8, 18)

DOW = [1.05, 1.05, 1.0, 0.95, 0.7, 0.4, 0.85]  # Mon..Sun
HOUR_WEIGHTS = {8: 2, 9: 3, 10: 5, 11: 6, 12: 6, 13: 7, 14: 9, 15: 9, 16: 8, 17: 6, 18: 6, 19: 8, 20: 7, 21: 5, 22: 2}
DURATIONS = ([0.5, 1.0, 1.5, 2.0, 3.0], [0.05, 0.38, 0.12, 0.33, 0.12])
OLD_ROOMS = {f"Room {n}": (8 if n in (204, 207, 210) else 4, w) for n, w in zip(
    range(201, 213), [1.0, 0.9, 1.1, 1.6, 1.0, 0.8, 1.5, 0.9, 1.0, 1.4, 0.7, 0.8])}
NEW_ROOMS = {f"Room {n}": (6, w) for n, w in zip(range(301, 305), [1.3, 1.2, 1.1, 1.0])}


def booking_rate(d: date) -> float:
    base = 13.0 * DOW[d.weekday()]
    if in_any(d, SEMESTERS):
        mult = 1.0
        if in_any(d, FINALS):
            mult = 1.6
        elif in_any(d, MIDTERMS):
            mult = 1.25
        elif in_any(d, SPRING_BREAKS):
            mult = 0.3
        elif in_any(d, THANKSGIVING):
            mult = 0.2
        elif in_any(d, FIRST_WEEKS):
            mult = 0.7
    elif d.month == 12 or (d.month == 1 and d.day < 8):
        mult = 0.12  # winter break
    else:
        mult = 0.3  # summer sessions
    years = (d - date(2024, 1, 1)).days / 365.25
    growth = 1.06**years
    rooms = 1.22 if d >= NEW_ROOMS_OPEN else 1.0
    return base * mult * growth * rooms


def make_bookings() -> pd.DataFrame:
    rows = []
    hours = np.array(list(HOUR_WEIGHTS))
    hour_p = np.array(list(HOUR_WEIGHTS.values()), float)
    for d in days("2024-01-08", "2026-09-30"):
        rooms = dict(OLD_ROOMS)
        if d >= NEW_ROOMS_OPEN:
            rooms |= NEW_ROOMS
        names = list(rooms)
        room_p = np.array([rooms[r][1] for r in names])
        weekend = d.weekday() >= 5
        hp = hour_p.copy()
        if weekend:
            hp[hours < 11] = 0  # rooms open at 11 on weekends
        taken: dict[str, list[tuple[int, int]]] = {r: [] for r in names}
        for _ in range(rng.poisson(booking_rate(d))):
            hour = int(rng.choice(hours, p=hp / hp.sum()))
            minute = 30 if rng.random() < 0.3 else 0
            length = float(rng.choice(DURATIONS[0], p=DURATIONS[1]))
            length = min(length, 24 - hour - minute / 60)  # last booking ends at midnight
            start = hour * 60 + minute
            end = start + int(length * 60)
            # The booking system won't double-book a room: pick among rooms free for the whole slot.
            free = np.array([all(end <= s or start >= e for s, e in taken[r]) for r in names])
            if not free.any():
                continue  # every room is taken; the request never becomes a booking
            p = room_p * free
            room = str(rng.choice(names, p=p / p.sum()))
            taken[room].append((start, end))
            cap = rooms[room][0]
            size = int(np.clip(rng.poisson(1.2 + cap / 3), 1, cap))
            who = str(rng.choice(["Undergraduate", "Graduate", "Faculty/Staff"], p=[0.68, 0.27, 0.05]))
            rows.append((d, f"{hour:02d}:{minute:02d}", length, room, size, who))
    rows.sort(key=lambda r: (r[0], r[1]))
    df = pd.DataFrame(rows, columns=["date", "start_time", "hours", "room", "group_size", "booked_by"])
    df.insert(0, "booking_id", [f"SR-{10001 + i}" for i in range(len(df))])
    df["date"] = df["date"].map(date.isoformat)
    df["hours"] = df["hours"].map(lambda h: f"{h:g}")
    df["group_size"] = df["group_size"].astype("object")
    df.loc[rng.random(len(df)) < 0.03, "group_size"] = ""  # some kiosks didn't ask

    # Messy labels: the old kiosk (replaced Jan 2025) wrote "Rm 204" instead of "Room 204".
    old_kiosk = (df["date"] < "2025-01-01") & (rng.random(len(df)) < 0.06)
    df.loc[old_kiosk, "room"] = df.loc[old_kiosk, "room"].str.replace("Room ", "Rm ", regex=False)
    return df


def add_duplicates(df: pd.DataFrame, share: float) -> pd.DataFrame:
    """The export repeats a booking that was edited after it was made: same row, twice."""
    pick = rng.random(len(df)) < share
    pick[:200] = False  # keep the first screenful clean, as real glitches rarely sit on top
    parts = []
    for i, row in enumerate(df.itertuples(index=False)):
        parts.append(row)
        if pick[i]:
            parts.append(row)
    return pd.DataFrame(parts, columns=df.columns)


def fiscal_year(iso: pd.Series) -> pd.Series:
    d = pd.to_datetime(iso)
    return d.dt.year + (d.dt.month >= 7).astype(int)


def bookings_key(clean: pd.DataFrame, raw: pd.DataFrame) -> dict:
    def counts(frame: pd.DataFrame) -> dict:
        fy = fiscal_year(frame["date"]).value_counts().sort_index()
        cy = pd.to_datetime(frame["date"]).dt.year.value_counts().sort_index()
        return {"fiscal": {f"FY{k}": int(v) for k, v in fy.items()}, "calendar": {str(k): int(v) for k, v in cy.items()}}

    room = clean["room"].str.replace("Rm ", "Room ", regex=False)
    top_rooms = room.value_counts().head(5)
    when = pd.to_datetime(clean["date"])
    fy26 = clean[fiscal_year(clean["date"]) == 2026]
    by_dow = pd.to_datetime(fy26["date"]).dt.day_name().value_counts()
    by_hour = fy26["start_time"].str[:2].astype(int).value_counts()
    return {
        "rows_in_file": len(raw),
        "unique_bookings": int(raw["booking_id"].nunique()),
        "duplicate_rows": int(len(raw) - raw["booking_id"].nunique()),
        "first_date": raw["date"].min(),
        "last_date": raw["date"].max(),
        "correct": counts(clean),
        "with_duplicates": counts(raw),
        "fy2026_growth_pct": round(100 * (counts(clean)["fiscal"]["FY2026"] / counts(clean)["fiscal"]["FY2025"] - 1), 1),
        "cy2025_growth_pct": round(100 * (counts(clean)["calendar"]["2025"] / counts(clean)["calendar"]["2024"] - 1), 1),
        "old_room_labels": int(raw["room"].str.startswith("Rm ").sum()),
        "top_rooms_all_time": {k: int(v) for k, v in top_rooms.items()},
        "fy2026_busiest_day": by_dow.idxmax(),
        "fy2026_busiest_start_hour": int(by_hour.idxmax()),
        "blank_group_size": int((raw["group_size"] == "").sum()),
        "span_days": int((when.max() - when.min()).days + 1),
    }


# ---------------------------------------------------------------------------------------------
# Campus cafe: Aug 18, 2025 to May 8, 2026, one row per menu item per day
# ---------------------------------------------------------------------------------------------

CLOSED = [
    ("2025-09-01", "2025-09-01"),  # Labor Day
    ("2025-10-16", "2025-10-17"),  # Fall break
    ("2025-11-26", "2025-11-28"),  # Thanksgiving
    ("2025-12-17", "2026-01-06"),  # Winter break
    ("2026-01-19", "2026-01-19"),  # MLK Day
    ("2026-03-09", "2026-03-13"),  # Spring break
]
EXAM_WEEKS = [
    ("2025-10-06", "2025-10-10"),  # Fall midterms
    ("2025-12-08", "2025-12-16"),  # Fall finals
    ("2026-03-02", "2026-03-06"),  # Spring midterms
    ("2026-04-28", "2026-05-07"),  # Spring finals
]
FALL = ("2025-08-18", "2025-12-16")
CAFE_DOW = [1.0, 1.05, 1.0, 0.95, 0.8, 0.4, 0.5]
PRICE_CHANGE = date(2026, 1, 7)
RENAME = date(2026, 1, 7)  # the new register calls it "Cold Brew Coffee"
TYPO = (date(2025, 9, 16), "Latte", 45.00)
# name, category, price before Jan 7, price after, base units per weekday, temperature response
MENU = [
    ("Drip Coffee", "Coffee", 2.25, 2.50, 110, "hot"),
    ("Latte", "Coffee", 4.50, 4.75, 65, "hot"),
    ("Cold Brew", "Coffee", 4.25, 4.50, 45, "cold"),
    ("Chai Latte", "Tea", 4.75, 4.75, 28, "hot"),
    ("Iced Tea", "Tea", 2.75, 2.75, 24, "cold"),
    ("Hot Chocolate", "Other drinks", 3.50, 3.50, 16, "very hot"),
    ("Croissant", "Bakery", 3.25, 3.25, 38, ""),
    ("Blueberry Muffin", "Bakery", 3.00, 3.00, 34, ""),
    ("Bagel", "Bakery", 2.75, 2.75, 30, ""),
    ("Breakfast Sandwich", "Food", 6.50, 6.50, 26, ""),
]
EXAM_LIFT = {"Coffee": 1.3, "Tea": 1.25, "Other drinks": 1.1, "Bakery": 1.1, "Food": 1.05}
# Busy days that aren't exams. The café sits between the career center and the stadium, so events bring crowds
# too. They keep the exam weeks from being the only bumps in the data: dates read off the sales spikes come out
# wrong, and only the manager's calendar gets them right.
EVENTS = [
    ("2025-09-23", "2025-09-24", 1.35),  # fall career fair
    ("2025-10-20", "2025-10-24", 1.4),  # homecoming week
    ("2026-02-10", "2026-02-12", 1.35),  # spring career and internship fair
    ("2026-04-11", "2026-04-11", 2.2),  # admitted students day (a Saturday)
]


def high_temp(d: date) -> int:
    doy = d.timetuple().tm_yday
    normal = 70.5 + 19.5 * np.cos(2 * np.pi * (doy - 196) / 365)
    return int(round(normal + rng.normal(0, 6)))


def temp_lift(kind: str, t: int) -> float:
    if kind == "hot":
        return max(0.6, 1 + 0.012 * (70 - t))
    if kind == "very hot":
        return max(0.25, 1 + 0.035 * (70 - t))
    if kind == "cold":
        return max(0.35, 1 + 0.02 * (t - 70))
    return 1.0


def make_cafe() -> pd.DataFrame:
    rows = []
    for d in days("2025-08-18", "2026-05-08"):
        t = high_temp(d)
        closed = in_any(d, CLOSED)
        exam = in_any(d, EXAM_WEEKS)
        first_week = d <= date(2025, 8, 24) or date(2026, 1, 7) <= d <= date(2026, 1, 13)
        for name, cat, p0, p1, base, kind in MENU:
            price = p1 if d >= PRICE_CHANGE else p0
            if closed:
                units = 0
            else:
                lam = base * CAFE_DOW[d.weekday()] * temp_lift(kind, t)
                lam *= EXAM_LIFT[cat] if exam else 1.0
                lam *= 1.15 if first_week else 1.0
                lam *= next((m for a, b, m in EVENTS if in_any(d, [(a, b)])), 1.0)
                units = int(rng.poisson(lam))
            label = "Cold Brew Coffee" if (name == "Cold Brew" and d >= RENAME) else name
            if (d, name) == TYPO[:2]:
                price = TYPO[2]
            rows.append((d.isoformat(), label, cat, units, f"{price:.2f}", t))
    return pd.DataFrame(rows, columns=["date", "item", "category", "units_sold", "unit_price", "high_temp_f"])


def cafe_key(df: pd.DataFrame) -> dict:
    df = df.copy()
    df["unit_price"] = df["unit_price"].astype(float)
    fixed = df.copy()
    typo_row = (fixed["date"] == TYPO[0].isoformat()) & (fixed["item"] == TYPO[1])
    fixed.loc[typo_row, "unit_price"] = 4.50
    for frame in (df, fixed):
        frame["revenue"] = frame["units_sold"] * frame["unit_price"]

    def fall_total(frame: pd.DataFrame) -> float:
        f = frame[(frame["date"] >= FALL[0]) & (frame["date"] <= FALL[1])]
        return round(float(f["revenue"].sum()), 2)

    daily = fixed.groupby("date")["revenue"].sum()
    dates = pd.Series([date.fromisoformat(s) for s in daily.index], index=daily.index)
    is_exam = dates.map(lambda d: in_any(d, EXAM_WEEKS))
    is_open = daily > 0

    def lift(include_closed: bool, frame_daily: pd.Series) -> dict:
        mask = pd.Series(True, index=frame_daily.index) if include_closed else is_open
        exam_avg = frame_daily[is_exam & mask].mean()
        other_avg = frame_daily[~is_exam & mask].mean()
        return {"exam_avg": round(float(exam_avg), 2), "other_avg": round(float(other_avg), 2),
                "lift_pct": round(100 * (exam_avg / other_avg - 1), 1)}

    # The weeks a reader would pick out as "busy" from the sales alone (Mon-Fri, open days, mean daily sales).
    weekday_open = daily[is_open & dates.map(lambda d: d.weekday() < 5)]
    week_start = pd.Series([date.fromisoformat(s) - timedelta(date.fromisoformat(s).weekday()) for s in weekday_open.index],
                           index=weekday_open.index)
    busiest_weeks = weekday_open.groupby(week_start).mean().sort_values(ascending=False).head(6)
    raw_daily = df.groupby("date")["revenue"].sum()
    items = fixed.assign(item=fixed["item"].replace({"Cold Brew Coffee": "Cold Brew"}))
    by_item = items.groupby("item")["revenue"].sum().sort_values(ascending=False)
    typo_units = int(df.loc[typo_row, "units_sold"].iloc[0])
    return {
        "rows_in_file": len(df),
        "first_date": df["date"].min(),
        "last_date": df["date"].max(),
        "closed_days": int((~is_open).sum()),
        "open_days": int(is_open.sum()),
        "fall_total_correct": fall_total(fixed),
        "fall_total_with_typo": fall_total(df),
        "typo": {"date": TYPO[0].isoformat(), "item": TYPO[1], "price_in_file": TYPO[2], "units": typo_units,
                 "extra_revenue": round(typo_units * (TYPO[2] - 4.50), 2),
                 "day_total_in_file": round(float(raw_daily[TYPO[0].isoformat()]), 2),
                 "day_total_correct": round(float(daily[TYPO[0].isoformat()]), 2)},
        "year_total_correct": round(float(fixed["revenue"].sum()), 2),
        "exam_lift_correct": lift(False, daily),
        "exam_lift_including_closed_days": lift(True, daily),
        "exam_lift_with_typo": lift(False, raw_daily),
        "best_seller_revenue": {k: round(float(v), 2) for k, v in by_item.head(3).items()},
        "best_seller_units": items.groupby("item")["units_sold"].sum().sort_values(ascending=False).head(1).index[0],
        "renamed_item_rows": int((df["item"] == "Cold Brew Coffee").sum()),
        "busiest_weeks_by_sales": {f"week of {k.isoformat()}" + (" (exam)" if in_any(k, EXAM_WEEKS) or
                                   in_any(k + timedelta(1), EXAM_WEEKS) else ""): round(float(v), 2)
                                   for k, v in busiest_weeks.items()},
        "busiest_open_day": daily.idxmax(),
        "busiest_open_day_total": round(float(daily.max()), 2),
    }


def main() -> None:
    global rng  # each dataset gets its own seed, so changing one never reshuffles the other
    rng = np.random.default_rng(20261015)
    clean = make_bookings()
    raw = add_duplicates(clean, 0.035)
    out = ROOT / "starters" / "study-rooms"
    out.mkdir(parents=True, exist_ok=True)
    raw.to_csv(out / "room_bookings.csv", index=False)

    rng = np.random.default_rng(20261016)
    cafe = make_cafe()
    out = ROOT / "starters" / "cafe"
    out.mkdir(parents=True, exist_ok=True)
    cafe.to_csv(out / "cafe_sales.csv", index=False)

    clean_dedup = raw.drop_duplicates()
    key = {"study_rooms": bookings_key(clean_dedup, raw), "cafe": cafe_key(cafe)}
    (ROOT / "instructor").mkdir(exist_ok=True)
    (ROOT / "instructor" / "answer-keys.json").write_text(json.dumps(key, indent=2) + "\n")
    print(json.dumps(key, indent=2))


if __name__ == "__main__":
    main()
