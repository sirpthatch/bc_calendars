"""Generate an ICS calendar for Juniper's spring 2026 specials schedule."""

from datetime import date, datetime
from icalendar import Calendar, Event

# A/B week specials lookup
SPECIALS = {
    "A": {
        0: "PE",                          # Monday
        1: "Swim & Spanish",              # Tuesday
        2: "Music & Library",             # Wednesday
        3: "Dance & STEAM",               # Thursday
        4: "Music, Library, & Spanish",   # Friday
    },
    "B": {
        0: "PE & STEAM",                  # Monday
        1: "Swim & Spanish",              # Tuesday
        2: "Music & Library",             # Wednesday
        3: "PE & Spanish",                # Thursday
        4: "Spanish & Dance",             # Friday
    },
}


def parse_school_days(path: str) -> dict[date, str]:
    """Parse calendar_test.ics and return {date: 'A'|'B'} for days after today."""
    from icalendar import Calendar as Cal

    with open(path, "rb") as f:
        cal = Cal.from_ical(f.read())

    today = date.today()

    # Collect all school dates and any A/B labels found
    date_labels: dict[date, str | None] = {}
    for comp in cal.walk("VEVENT"):
        desc = str(comp.get("DESCRIPTION", ""))
        dt = comp.get("DTSTART").dt
        d = dt.date() if isinstance(dt, datetime) else dt

        if d <= today:
            continue

        # Track that this date is a school day
        if d not in date_labels:
            date_labels[d] = None

        # Extract A/B if present
        if "Day:" in desc:
            day_val = desc.split("Day:")[1].split(";")[0].strip().rstrip("\\")
            if "-A" in day_val:
                date_labels[d] = "A"
            elif "-B" in day_val:
                date_labels[d] = "B"

    # Propagate A/B to unlabeled days by using the week's labeled days
    sorted_dates = sorted(date_labels.keys())
    for d in sorted_dates:
        if date_labels[d] is not None:
            continue
        # Find another day in the same ISO week that has a label
        iso_week = d.isocalendar()[1]
        iso_year = d.isocalendar()[0]
        for other in sorted_dates:
            if (
                other.isocalendar()[0] == iso_year
                and other.isocalendar()[1] == iso_week
                and date_labels[other] is not None
            ):
                date_labels[d] = date_labels[other]
                break

    # Filter out any days we still couldn't label
    return {d: ab for d, ab in date_labels.items() if ab is not None}


def main() -> None:
    school_days = parse_school_days("lib/calendar_test.ics")

    cal = Calendar()
    cal.add("prodid", "-//Juniper Specials//EN")
    cal.add("version", "2.0")
    cal.add("calscale", "GREGORIAN")
    cal.add("x-wr-calname", "J - Specials Spring 2026")
    cal.add("x-wr-timezone", "America/New_York")

    count = 0
    for d in sorted(school_days):
        ab = school_days[d]
        weekday = d.weekday()
        if weekday not in SPECIALS[ab]:
            continue

        special_name = SPECIALS[ab][weekday]
        event = Event()
        event.add("summary", f"J - {special_name}")
        event.add("dtstart", d)
        event.add("dtend", d)
        event.add("uid", f"juniper-specials-{d.isoformat()}")
        event.add("dtstamp", datetime.now())
        cal.add_component(event)
        count += 1

    out_path = "output/juniper_spring_specials.ics"
    with open(out_path, "wb") as f:
        f.write(cal.to_ical())

    print(f"Wrote {count} events to {out_path}")

    # Summary by A/B
    a_count = sum(1 for d in school_days if school_days[d] == "A" and d.weekday() < 5)
    b_count = sum(1 for d in school_days if school_days[d] == "B" and d.weekday() < 5)
    print(f"  A-week days: {a_count}")
    print(f"  B-week days: {b_count}")


if __name__ == "__main__":
    main()
