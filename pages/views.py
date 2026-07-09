from datetime import date
from collections import defaultdict

from django.shortcuts import render

from .placeholder_data import SCHEDULE_ENTRIES, GURDWARA_INFO


def _upcoming(entries):
    today = date.today()
    result = [e for e in entries if e["date"] >= today]
    result.sort(key=lambda e: (e["date"], e["start_time"]))
    return result


def _group_by_day(entries):
    groups = defaultdict(list)
    for entry in entries:
        groups[entry["date"]].append(entry)
    return sorted(groups.items())


def home(request):
    upcoming = _upcoming(SCHEDULE_ENTRIES)
    return render(request, "home.html", {
        "current_page": "home",
        "preview_entries": upcoming[:3],
        "gurdwara": GURDWARA_INFO,
    })


def schedule(request):
    upcoming = _upcoming(SCHEDULE_ENTRIES)
    return render(request, "schedule.html", {
        "current_page": "schedule",
        "days": _group_by_day(upcoming),
        "gurdwara": GURDWARA_INFO,
    })


def school(request):
    school_entries = [
        e for e in _upcoming(SCHEDULE_ENTRIES) if e["category"] == "School"
    ]
    return render(request, "school.html", {
        "current_page": "school",
        "school_entries": school_entries,
        "gurdwara": GURDWARA_INFO,
    })


def livestream(request):
    return render(request, "livestream.html", {
        "current_page": "livestream",
        "gurdwara": GURDWARA_INFO,
    })


def contact(request):
    return render(request, "contact.html", {
        "current_page": "contact",
        "gurdwara": GURDWARA_INFO,
    })
