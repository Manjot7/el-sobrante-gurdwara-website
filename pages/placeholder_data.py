"""
Placeholder data matching the ScheduleEntry model shape from PRD section 7.
Swapping in real Wagtail data later = wiring these templates to a queryset,
not a template rewrite.

ScheduleEntry fields:
    title        str
    date         datetime.date
    start_time   datetime.time
    end_time     datetime.time | None
    location     str
    category     "Diwan" | "Langar" | "School" | "Special Event"
    is_featured  bool
    notes        str
"""

from datetime import date, time

GURDWARA_INFO = {
    "name": "El Sobrante Gurdwara Sahib",
    "address_line1": "3550 Hillcrest Rd",
    "address_line2": "El Sobrante, CA 94803",
    "phone_main": "(510) 223-9987",
    "phone_alt": "(510) 223-1102",
    "email": "info@thesikhcenter.com",
    "website": "https://thesikhcenter.com",
    "youtube_channel_url": "https://www.youtube.com/c/ElSobranteGurdwaraSahib",
    "youtube_channel_id": "UCx1y5VenBaV9WspiK_oAnxQ",
    "youtube_live_video_id": "Jvebt007X4M",
    "facebook_url": "https://www.facebook.com/sfsikhcenter",
    "maps_directions_url": (
        "https://www.google.com/maps/search/?api=1"
        "&query=3550+Hillcrest+Rd+El+Sobrante+CA+94803"
    ),
}

# All entries for the current two-week window (week of Jul 6 + Jul 13, 2026).
# Past entries are filtered out automatically in views.py — nothing is deleted here.
SCHEDULE_ENTRIES = [
    # ── Wednesday Jul 9 ──────────────────────────────────────────────────────
    {
        "title": "Midweek Nitnem & Kirtan",
        "date": date(2026, 7, 9),
        "start_time": time(18, 30),
        "end_time": time(20, 0),
        "location": "Main Hall",
        "category": "Diwan",
        "is_featured": False,
        "notes": "Short evening prayer and kirtan session. All are welcome.",
    },
    # ── Saturday Jul 11 ──────────────────────────────────────────────────────
    {
        "title": "Gurpurab — Guru Hargobind Sahib Ji",
        "date": date(2026, 7, 11),
        "start_time": time(8, 0),
        "end_time": time(13, 0),
        "location": "Main Hall",
        "category": "Special Event",
        "is_featured": True,
        "notes": (
            "Akhand Path Bhog, kirtan, ardas, and hukamnama. "
            "Please join us to celebrate Guru Hargobind Sahib Ji's Gurgaddi Diwas."
        ),
    },
    {
        "title": "Special Langar",
        "date": date(2026, 7, 11),
        "start_time": time(13, 0),
        "end_time": time(15, 0),
        "location": "Langar Hall",
        "category": "Langar",
        "is_featured": True,
        "notes": "Extended langar served in celebration of Gurpurab. All sangat welcome.",
    },
    # ── Sunday Jul 13 ────────────────────────────────────────────────────────
    {
        "title": "Asa Di Var",
        "date": date(2026, 7, 13),
        "start_time": time(9, 0),
        "end_time": time(10, 30),
        "location": "Main Hall",
        "category": "Diwan",
        "is_featured": False,
        "notes": "Morning prayer — Asa Di Var paath and kirtan.",
    },
    {
        "title": "Khalsa School",
        "date": date(2026, 7, 13),
        "start_time": time(10, 0),
        "end_time": time(12, 0),
        "location": "Classroom (Room 2)",
        "category": "School",
        "is_featured": False,
        "notes": "Punjabi language, Gurmukhi script, and Sikh history for ages 5–14.",
    },
    {
        "title": "Sunday Diwan",
        "date": date(2026, 7, 13),
        "start_time": time(10, 30),
        "end_time": time(12, 30),
        "location": "Main Hall",
        "category": "Diwan",
        "is_featured": False,
        "notes": "Katha, ardas, and hukamnama.",
    },
    {
        "title": "Langar Seva",
        "date": date(2026, 7, 13),
        "start_time": time(12, 30),
        "end_time": time(14, 0),
        "location": "Langar Hall",
        "category": "Langar",
        "is_featured": False,
        "notes": "Community kitchen — free meal served to all visitors.",
    },
    # ── Wednesday Jul 16 ─────────────────────────────────────────────────────
    {
        "title": "Midweek Nitnem & Kirtan",
        "date": date(2026, 7, 16),
        "start_time": time(18, 30),
        "end_time": time(20, 0),
        "location": "Main Hall",
        "category": "Diwan",
        "is_featured": False,
        "notes": "Short evening prayer and kirtan session.",
    },
    # ── Sunday Jul 20 ────────────────────────────────────────────────────────
    {
        "title": "Asa Di Var",
        "date": date(2026, 7, 20),
        "start_time": time(9, 0),
        "end_time": time(10, 30),
        "location": "Main Hall",
        "category": "Diwan",
        "is_featured": False,
        "notes": "Morning prayer — Asa Di Var paath and kirtan.",
    },
    {
        "title": "Khalsa School",
        "date": date(2026, 7, 20),
        "start_time": time(10, 0),
        "end_time": time(12, 0),
        "location": "Classroom (Room 2)",
        "category": "School",
        "is_featured": False,
        "notes": "Punjabi language, Gurmukhi script, and Sikh history for ages 5–14.",
    },
    {
        "title": "Sunday Diwan",
        "date": date(2026, 7, 20),
        "start_time": time(10, 30),
        "end_time": time(12, 30),
        "location": "Main Hall",
        "category": "Diwan",
        "is_featured": False,
        "notes": "Katha, ardas, and hukamnama.",
    },
    {
        "title": "Langar Seva",
        "date": date(2026, 7, 20),
        "start_time": time(12, 30),
        "end_time": time(14, 0),
        "location": "Langar Hall",
        "category": "Langar",
        "is_featured": False,
        "notes": "Community kitchen — free meal served to all visitors.",
    },
    # ── Wednesday Jul 23 ─────────────────────────────────────────────────────
    {
        "title": "Midweek Nitnem & Kirtan",
        "date": date(2026, 7, 23),
        "start_time": time(18, 30),
        "end_time": time(20, 0),
        "location": "Main Hall",
        "category": "Diwan",
        "is_featured": False,
        "notes": "Short evening prayer and kirtan session.",
    },
]
