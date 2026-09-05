"""
Seed the database with the content we already have.

Safe to re-run: it never overwrites something an editor has changed, it only
fills in what is missing.
"""

from pathlib import Path

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from content.models import Photo, ProgramItem, SiteSettings

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
