"""
Seed the database with the content we already have.

Safe to re-run: it never overwrites something an editor has changed, it only
fills in what is missing.
"""

from pathlib import Path

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from content.models import PageText, Photo, ProgramItem, SiteSettings, Stat

# Ordered roughly chronologically, so the carousel tells the story in sequence.
# The captions are already printed into these scans, so the caption stored here
# is used only as alt text for screen readers — the template does not draw it.
HISTORY_PHOTOS = [
    ("Foundation Stone Laying by Panj Pyaras.jpeg", "Foundation stone laid by the Panj Pyaras"),
    ("Outdoor Cooking before building.jpeg", "Langar cooked outdoors, before the building"),
    ("First Akhand Path in Tent.jpeg", "The first Akhand Path, held in a tent"),
    ("Kar Sewa During First Phase Construction.jpeg", "Kar sewa during first phase construction"),
    ("First Phase Building Under Construction.jpeg", "First phase of the building under construction"),
    ("First Phase Building Under Construction 2.jpeg", "First phase construction continues"),
    ("Nishan Sahib Installation.jpeg", "Installation of the Nishan Sahib"),
    ("Hall Kirtan.jpeg", "Kirtan in the original hall"),
    ("1988 Vaisakhi Ardaas after changing Nishaan Sahib Chola Sahib.jpeg",
     "Vaisakhi ardaas after the Nishan Sahib chola was changed, 1988"),
]

# The only current photo of the building we have a clear licence for. It is
# CC BY-SA 3.0, so the credit below must stay visible on the site — see the
# footer. Replace this once the committee supplies its own photos, and the
# credit can then go.
HERO_PHOTOS = [
    (
        "gurdwara-cropped-commons.jpg",
        "Gurdwara Sahib El Sobrante seen from the hillside",
        "Photo: Coro, CC BY-SA 3.0, via Wikimedia Commons",
    ),
]

# The wording that used to be hardcoded in the templates. Seeded once, then
# owned by the committee — `get_or_create` means a later edit is never
# overwritten by a redeploy.
PAGE_TEXT = [
    (PageText.HOME_ABOUT, "About the Gurdwara", """The Sikh Center of SF Bay Area, home of Gurdwara Sahib El Sobrante, has been serving the Bay Area Sikh community since its establishment in 1969. What began as informal gatherings in Berkeley grew into a formal organization with one purpose: to give the Bay Area's growing Sikh population a dedicated place of worship.

In 1976, approximately five acres of hillside in El Sobrante were purchased for the Gurdwara. The first building phase was completed in May 1979, and the current structure, with its golden domes and views over the El Sobrante valley and San Pablo Bay, was completed in June 1992.

Rooted in the teachings of Sri Guru Granth Sahib Ji, the Gurdwara is open to all regardless of faith or background. Langar, a free community meal, is served daily to every visitor."""),
    (PageText.HOME_VISIT, "Find the Gurdwara",
     "Situated in the hills of El Sobrante, 25 miles north of San Francisco. "
     "Free parking available on-site."),
    (PageText.SCHEDULE_HEADER, "Daily Programme",
     "Langar is served daily to all visitors."),
    (PageText.EVENTS_HEADER, "Events & Calendar",
     "Upcoming programs, Gurpurabs, and the paths booked by the sangat."),
    (PageText.EVENTS_CALENDAR, "Gurdwara Calendar",
     "Akhand Paath, Sehaj Paath, Sukhmani Sahib and Anand Karaj bookings, "
     "alongside Gurpurab and Nanakshahi dates."),
    (PageText.LIVESTREAM_HEADER, "Livestream",
     "Daily live diwan on YouTube, morning and evening, 7 days a week."),
    (PageText.LIVESTREAM_PROGRAM, "Daily Live Program",
     "7 days a week, streamed live from the Gurdwara."),
    (PageText.CONTACT_HEADER, "Contact & Directions",
     "All are welcome."),
    (PageText.CONTACT_PARKING, "Parking & Access", """Free on-site parking lot on Hillcrest Rd
Located in the hills of El Sobrante, 25 miles north of San Francisco
Panoramic views of the El Sobrante valley and San Pablo Bay from the grounds"""),
    (PageText.CONTACT_EXPECT, "What to Expect", """Head coverings required inside the Darbar Sahib (available at entry)
Shoes removed before entering (racks provided at the entrance)
Langar (free meal) served after Sunday Diwan, all are welcome
All faiths and backgrounds welcome, no prior knowledge of Sikhism needed"""),
]

STATS = [
    ("1969", "Year established", 10),
    ("5 acres", "Hilltop grounds in El Sobrante", 20),
    ("Daily", "Free langar for all visitors", 30),
]


PROGRAM_ITEMS = [
    {
        "heading": "Morning Program",
        "days": "Daily",
        "items": "Nitnem · Asa Di Vaar · Ardas · Hukamnama",
        "sort_order": 10,
        "is_highlighted": False,
    },
    {
        "heading": "Evening Program",
        "days": "Daily",
        "items": (
            "Rehrass Sahib · Aarti · Kirtan · Katha · Ardas · Hukamnama · "
            "Kirtan Sohila · Samapti"
        ),
        "sort_order": 20,
        "is_highlighted": False,
    },
    {
        "heading": "Wednesday & Friday",
        "days": "Additional program",
        "items": (
            "Sukhmani Sahib · Rehrass Sahib · Kirtan · Katha · Ardas · "
            "Hukamnama · Kirtan Sohila"
        ),
        "sort_order": 30,
        "is_highlighted": True,
    },
]


class Command(BaseCommand):
    help = "Fill in the gurdwara details, daily programme and history photos."

    def handle(self, *args, **options):
        site = SiteSettings.load()
        self.stdout.write(self.style.SUCCESS(f"Gurdwara details ready: {site.name}"))

        created = 0
        for item in PROGRAM_ITEMS:
            _, was_created = ProgramItem.objects.get_or_create(
                heading=item["heading"], defaults=item
            )
            created += was_created
        self.stdout.write(
            self.style.SUCCESS(
                f"Daily programme: {created} row(s) added, "
                f"{ProgramItem.objects.count()} total."
            )
        )

        hero_dir = Path(settings.BASE_DIR) / "imgs" / "Gurdwara"
        added = 0
        for index, (filename, caption, credit) in enumerate(HERO_PHOTOS, start=1):
            path = hero_dir / filename
            if not path.exists():
                self.stdout.write(self.style.WARNING(f"  missing: {filename}"))
                continue
            if Photo.objects.filter(category=Photo.HERO, caption=caption).exists():
                continue
            photo = Photo(
                category=Photo.HERO,
                caption=caption,
                credit=credit,
                sort_order=index * 10,
            )
            photo.image = ContentFile(path.read_bytes(), name=path.name)
            photo.save()
            added += 1
        self.stdout.write(
            self.style.SUCCESS(
                f"Slideshow photos: {added} added, "
                f"{Photo.objects.filter(category=Photo.HERO).count()} total."
            )
        )

        created = 0
        for order, (key, heading, body) in enumerate(PAGE_TEXT, start=1):
            _, was_created = PageText.objects.get_or_create(
                key=key,
                defaults={"heading": heading, "body": body, "sort_order": order * 10},
            )
            created += was_created
        self.stdout.write(
            self.style.SUCCESS(
                f"Page text: {created} block(s) added, {PageText.objects.count()} total."
            )
        )

        created = 0
        for value, label, order in STATS:
            _, was_created = Stat.objects.get_or_create(
                value=value, defaults={"label": label, "sort_order": order}
            )
            created += was_created
        self.stdout.write(
            self.style.SUCCESS(
                f"Facts: {created} added, {Stat.objects.count()} total."
            )
        )

        # The archival scans are used exactly as supplied — white paper margins,
        # printed captions and all. The carousel sizes itself to each photo, so
        # nothing needs cropping to avoid empty space around it.
        source_dir = Path(settings.BASE_DIR) / "imgs" / "History"
        if not source_dir.exists():
            self.stdout.write(
                self.style.WARNING(f"No history photos found at {source_dir}")
            )
            return

        added = 0
        for index, (filename, caption) in enumerate(HISTORY_PHOTOS, start=1):
            path = source_dir / filename
            if not path.exists():
                self.stdout.write(self.style.WARNING(f"  missing: {filename}"))
                continue
            if Photo.objects.filter(category=Photo.HISTORY, caption=caption).exists():
                continue
            photo = Photo(
                category=Photo.HISTORY, caption=caption, sort_order=index * 10
            )
            # Assign rather than field.save(), so the file is only written to
            # storage once — after the resize in Photo.save().
            photo.image = ContentFile(path.read_bytes(), name=path.name)
            photo.save()
            added += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"History photos: {added} added, "
                f"{Photo.objects.filter(category=Photo.HISTORY).count()} total."
            )
        )
