"""Generate an ICS calendar for Juniper's spring 2026 afterschool programs."""

from datetime import date, datetime, timedelta
from icalendar import Calendar, Event
from zoneinfo import ZoneInfo

ET = ZoneInfo("America/New_York")

# Afterschool programs from spring_2026_afterschool.md
PROGRAMS = [
    {
        "name": "Junior Chefs",
        "location": "712 Carroll",
        "dates": [
            date(2026, 4, 6), date(2026, 4, 13), date(2026, 4, 20),
            date(2026, 5, 4), date(2026, 5, 11), date(2026, 5, 18),
            date(2026, 6, 1),
        ],
    },
    {
        "name": "Gymnastics",
        "location": "701 Carroll",
        "dates": [
            date(2026, 4, 7), date(2026, 4, 14), date(2026, 4, 21),
            date(2026, 4, 28), date(2026, 5, 5), date(2026, 5, 12),
            date(2026, 5, 19), date(2026, 5, 26), date(2026, 6, 2),
        ],
    },
    {
        "name": "Mini Book Making",
        "location": "701 Carroll",
        "dates": [
            date(2026, 4, 9), date(2026, 4, 16), date(2026, 4, 23),
            date(2026, 4, 30), date(2026, 5, 7), date(2026, 5, 14),
            date(2026, 5, 21), date(2026, 5, 28), date(2026, 6, 4),
        ],
    },
    {
        "name": "Colors, Shapes, and Design: Art",
        "location": "712 Carroll",
        "dates": [
            date(2026, 4, 10), date(2026, 4, 17), date(2026, 4, 24),
            date(2026, 5, 1), date(2026, 5, 8), date(2026, 5, 15),
            date(2026, 5, 22), date(2026, 5, 29), date(2026, 6, 5),
        ],
    },
]


def get_wednesday_dates_from_ics(path: str) -> list[date]:
    """Extract Wednesday school-day dates from the ICS within the spring window."""
    from icalendar import Calendar as Cal

    with open(path, "rb") as f:
        cal = Cal.from_ical(f.read())

    wednesdays: set[date] = set()
    for comp in cal.walk("VEVENT"):
        desc = str(comp.get("DESCRIPTION", ""))
        if "Wednesday" in desc:
            dt = comp.get("DTSTART").dt
            d = dt.date() if isinstance(dt, datetime) else dt
            if date(2026, 4, 1) <= d <= date(2026, 6, 10):
                wednesdays.add(d)

    return sorted(wednesdays)


def make_event(summary: str, location: str, d: date) -> Event:
    """Create a VEVENT from 3:00-4:30 PM ET on the given date."""
    event = Event()
    event.add("summary", f"J - {summary}")
    event.add("location", location)
    event.add("dtstart", datetime(d.year, d.month, d.day, 15, 0, tzinfo=ET))
    event.add("dtend", datetime(d.year, d.month, d.day, 16, 30, tzinfo=ET))
    event.add("dtstamp", datetime.now(tz=ET))
    event.add("uid", f"juniper-{summary.lower().replace(' ', '-')}-{d.isoformat()}")
    return event


def main() -> None:
    cal = Calendar()
    cal.add("prodid", "-//Juniper Afterschool//EN")
    cal.add("version", "2.0")
    cal.add("calscale", "GREGORIAN")
    cal.add("x-wr-calname", "J - Afterschool Spring 2026")
    cal.add("x-wr-timezone", "America/New_York")

    count = 0

    # Mon/Tue/Thu/Fri programs
    for prog in PROGRAMS:
        for d in prog["dates"]:
            cal.add_component(make_event(prog["name"], prog["location"], d))
            count += 1

    # Wednesday Playgroup
    wed_dates = get_wednesday_dates_from_ics("lib/calendar_test.ics")
    for d in wed_dates:
        cal.add_component(make_event("Playgroup", "701 Carroll Street", d))
        count += 1

    out_path = "lib/juniper_spring_afterschool.ics"
    with open(out_path, "wb") as f:
        f.write(cal.to_ical())

    print(f"Wrote {count} events to {out_path}")
    print(f"  Mon (Junior Chefs): {len(PROGRAMS[0]['dates'])}")
    print(f"  Tue (Gymnastics): {len(PROGRAMS[1]['dates'])}")
    print(f"  Wed (Playgroup): {len(wed_dates)}")
    print(f"  Thu (Mini Book Making): {len(PROGRAMS[2]['dates'])}")
    print(f"  Fri (Art): {len(PROGRAMS[3]['dates'])}")


if __name__ == "__main__":
    main()
