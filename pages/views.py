from django.shortcuts import render

from content.models import Event, Photo, ProgramItem


def _common():
    """Content shared by every page. `site` arrives via the context processor."""
    return {
        "program_items": ProgramItem.objects.all(),
    }


def home(request):
    return render(request, "home.html", {
        "current_page": "home",
        "hero_photos": Photo.objects.filter(category=Photo.HERO, is_active=True),
        "history_photos": Photo.objects.filter(category=Photo.HISTORY, is_active=True),
        "upcoming_events": Event.upcoming()[:3],
        **_common(),
    })


def schedule(request):
    return render(request, "schedule.html", {
        "current_page": "schedule",
        **_common(),
    })


def events(request):
    return render(request, "events.html", {
        "current_page": "events",
        "upcoming_events": Event.upcoming(),
        **_common(),
    })


def academy(request):
    return render(request, "academy.html", {
        "current_page": "academy",
        "academy_photos": Photo.objects.filter(
            category=Photo.ACADEMY, is_active=True
        ),
        **_common(),
    })


def livestream(request):
    return render(request, "livestream.html", {
        "current_page": "livestream",
        **_common(),
    })


def contact(request):
    return render(request, "contact.html", {
        "current_page": "contact",
        **_common(),
    })
