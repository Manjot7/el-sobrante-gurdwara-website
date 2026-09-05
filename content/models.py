"""
Content models for the Sikh Center of SF Bay Area website.

Four models, deliberately. Everything date-driven (path bookings, Anand Karaj,
Gurpurab dates) lives in Google Calendar, which the committee already knows how
to use. These models cover only what Google Calendar can't hold: photos, event
posters, the weekly programme, and the gurdwara's own details.

Field help_text throughout is written for a committee member who has never used
a CMS. Please keep it that way when adding fields.
"""

from io import BytesIO

from django.core.files.base import ContentFile
from django.db import models
from django.utils import timezone
from PIL import Image, ImageOps

# Committee members upload photos straight off a phone — often 8 MB or more,
# and frequently rotated via EXIF rather than actually being portrait. Left
# alone these make the homepage unusable on mobile data, so every upload is
# normalised on save. This is invisible to whoever uploaded it.
MAX_IMAGE_WIDTH = 2000
MAX_IMAGE_HEIGHT = 2000
JPEG_QUALITY = 82
# Below this, an image that already fits is left exactly as uploaded. Avoids
# recompressing an already-small file, which only loses quality.
RECOMPRESS_ABOVE_BYTES = 600 * 1024


def process_upload(image_field):
    """Rotate by EXIF, shrink to fit, and recompress. Returns True if changed."""
    try:
        image_field.open()
        img = Image.open(image_field)
        img.load()
    except (OSError, ValueError):
        # Not a readable image — let Django's own ImageField validation report it.
        return False

    has_alpha = img.mode in ("RGBA", "LA", "P")

    # Phone cameras record orientation in EXIF rather than rotating the pixels.
    needs_rotation = img.getexif().get(0x0112, 1) not in (1, 0)
    img = ImageOps.exif_transpose(img)

    oversized = img.width > MAX_IMAGE_WIDTH or img.height > MAX_IMAGE_HEIGHT
    try:
        heavy = image_field.size > RECOMPRESS_ABOVE_BYTES
    except (OSError, ValueError):
        heavy = True

    if not (oversized or heavy or needs_rotation):
        return False

    if has_alpha:
        img = img.convert("RGBA")
        fmt, ext, params = "PNG", "png", {"optimize": True}
    else:
        img = img.convert("RGB")
        fmt, ext, params = "JPEG", "jpg", {
            "quality": JPEG_QUALITY,
            "optimize": True,
            "progressive": True,
        }

    img.thumbnail((MAX_IMAGE_WIDTH, MAX_IMAGE_HEIGHT), Image.LANCZOS)

    buffer = BytesIO()
    img.save(buffer, format=fmt, **params)

    name = image_field.name.rsplit("/", 1)[-1].rsplit(".", 1)[0]
    image_field.save(f"{name}.{ext}", ContentFile(buffer.getvalue()), save=False)
    return True


class ImageProcessingMixin:
    """Normalises `image_fields` whenever a new file is uploaded."""

    image_fields = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_images = {f: getattr(self, f).name for f in self.image_fields}

    def save(self, *args, **kwargs):
        for field_name in self.image_fields:
            field = getattr(self, field_name)
            if field and field.name != self._original_images.get(field_name):
                process_upload(field)
        super().save(*args, **kwargs)
        self._original_images = {f: getattr(self, f).name for f in self.image_fields}


class SiteSettings(models.Model):
    """One row, ever. The gurdwara's own details, editable without code."""

    name = models.CharField(
        "Gurdwara name",
        max_length=120,
        default="Sikh Center of SF Bay Area",
        help_text="Shown in the top bar, the footer, and browser tabs.",
    )
    gurmukhi_name = models.CharField(
        "Name in Gurmukhi",
        max_length=120,
        blank=True,
        default="ਸਿੱਖ ਸੈਂਟਰ",
        help_text="Shown in smaller text under the name. Leave blank to hide it.",
    )
    location_line = models.CharField(
        "Location line",
        max_length=120,
        blank=True,
        default="Gurdwara Sahib El Sobrante",
        help_text="Shown under the gurdwara name, e.g. 'Gurdwara Sahib El Sobrante'.",
    )

    address_line1 = models.CharField(max_length=120, default="3550 Hillcrest Rd")
    address_line2 = models.CharField(max_length=120, default="El Sobrante, CA 94803")
    phone_main = models.CharField(
        "Main phone", max_length=40, default="(510) 223-9987"
    )
    phone_alt = models.CharField(
        "Second phone",
        max_length=40,
        blank=True,
        default="(510) 223-1102",
        help_text="Leave blank if there is only one number.",
    )
    email = models.EmailField(blank=True, default="info@thesikhcenter.com")

    opening_hours = models.CharField(
        max_length=120,
        blank=True,
        default="Open daily 5:00 AM – 8:30 PM",
        help_text="Shown on the Home and Contact pages.",
    )

    youtube_channel_id = models.CharField(
        "YouTube channel ID",
        max_length=64,
        blank=True,
        default="UCx1y5VenBaV9WspiK_oAnxQ",
        help_text=(
            "The livestream page always plays whatever is live on this channel, "
            "so it never needs changing when a new stream starts. Find it in "
            "YouTube Studio under Settings → Channel → Advanced settings."
        ),
    )
    youtube_channel_url = models.URLField(
        "YouTube channel link",
        blank=True,
        default="https://www.youtube.com/c/ElSobranteGurdwaraSahib",
        help_text="Used for the 'Open on YouTube' links.",
    )
    facebook_url = models.URLField(
        "Facebook page link", blank=True, default="https://www.facebook.com/sfsikhcenter"
    )

    google_calendar_id = models.CharField(
        "Google Calendar ID",
        max_length=200,
        blank=True,
        help_text=(
            "The gurdwara's own calendar, where paths and bookings are entered. "
            "In Google Calendar: Settings → click the calendar → 'Integrate "
            "calendar' → copy 'Calendar ID'. Leave blank to hide the calendar."
        ),
    )
    nanakshahi_calendar_id = models.CharField(
        "Nanakshahi calendar ID",
        max_length=200,
        blank=True,
        default="8lh6gp8c7pdm7ta30435i2k854@group.calendar.google.com",
        help_text=(
            "Adds Gurpurab and Nanakshahi dates on top of the gurdwara calendar. "
            "This updates itself every year — no action needed."
        ),
    )

    booking_note = models.CharField(
        max_length=200,
        blank=True,
        default="To book a path, please call the Gurdwara.",
        help_text="Shown above the calendar. Bookings are not taken on the website.",
    )

    class Meta:
        verbose_name = "Gurdwara details"
        verbose_name_plural = "Gurdwara details"

    def __str__(self):
        return self.name

    @staticmethod
    def _tel(number):
        digits = "".join(c for c in number if c.isdigit())
        return f"+1{digits}" if len(digits) == 10 else f"+{digits}"

    @property
    def phone_main_tel(self):
        return self._tel(self.phone_main) if self.phone_main else ""

    @property
    def phone_alt_tel(self):
        return self._tel(self.phone_alt) if self.phone_alt else ""

    @property
    def maps_directions_url(self):
        query = f"{self.address_line1} {self.address_line2}".replace(" ", "+")
        return f"https://www.google.com/maps/search/?api=1&query={query}"

    @property
    def maps_embed_url(self):
        query = f"{self.address_line1} {self.address_line2}".replace(" ", "+")
        return f"https://maps.google.com/maps?q={query}&t=&z=15&ie=UTF8&iwloc=&output=embed"

    @property
    def calendar_embed_url(self):
        """Both calendars in one embed. Public viewers get read-only access."""
        if not self.google_calendar_id:
            return ""
        sources = [self.google_calendar_id]
        if self.nanakshahi_calendar_id:
            sources.append(self.nanakshahi_calendar_id)
        params = "".join(f"&src={s}" for s in sources)
        return (
            "https://calendar.google.com/calendar/embed"
            f"?ctz=America/Los_Angeles&mode=MONTH&showTitle=0&showPrint=0"
            f"&showTabs=0&showCalendars=0{params}"
        )

    @property
    def youtube_live_embed_url(self):
        """Resolves to whatever is live now — never needs updating."""
        if not self.youtube_channel_id:
            return ""
        return (
            "https://www.youtube.com/embed/live_stream"
            f"?channel={self.youtube_channel_id}&rel=0"
        )

    def save(self, *args, **kwargs):
        # Enforce the singleton regardless of how the save was triggered.
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class Photo(ImageProcessingMixin, models.Model):
    """Every photo on the site. One upload form, a dropdown picks where it goes."""

    HERO = "hero"
    HISTORY = "history"
    ACADEMY = "academy"
    CATEGORY_CHOICES = [
        (HERO, "Home page slideshow"),
        (HISTORY, "History (About section)"),
        (ACADEMY, "Khalsa Academy gallery"),
    ]

    image_fields = ("image",)

    # width_field/height_field cache the dimensions in the database. Without
    # them the history carousel would open all nine image files on every
    # single page load just to find their shapes.
    image = models.ImageField(
        upload_to="photos/",
        width_field="image_width",
        height_field="image_height",
        help_text="Large, landscape photos look best. Big files are fine — "
        "they are shrunk automatically.",
    )
    image_width = models.PositiveIntegerField(null=True, blank=True, editable=False)
    image_height = models.PositiveIntegerField(null=True, blank=True, editable=False)
    category = models.CharField(
        "Where it appears",
        max_length=20,
        choices=CATEGORY_CHOICES,
        default=HERO,
    )
    caption = models.CharField(
        max_length=200,
        blank=True,
        help_text="A short description of the photo. Always read out by screen "
        "readers. Shown on the page for History and Academy photos; the home "
        "page slideshow deliberately shows no text.",
    )
    credit = models.CharField(
        "Photo credit",
        max_length=200,
        blank=True,
        help_text="Only needed for photos taken by someone outside the "
        "gurdwara. Shown in small text in the footer.",
    )
    sort_order = models.PositiveIntegerField(
        "Order",
        default=0,
        help_text="Lower numbers show first. Change the numbers to reorder.",
    )
    is_active = models.BooleanField(
        "Show on the website",
        default=True,
        help_text="Untick to hide the photo without deleting it.",
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["sort_order", "id"]
        verbose_name = "Photo"
        verbose_name_plural = "Photos on the website"

    def __str__(self):
        return self.caption or f"{self.get_category_display()} photo #{self.pk}"


class Event(ImageProcessingMixin, models.Model):
    """A handful of major events a year, each with a poster.

    Routine bookings belong in Google Calendar, not here — this is for the
    events that warrant a poster on the home page.
    """

    image_fields = ("image",)

    title = models.CharField(max_length=200)
    date = models.DateField("Date", help_text="The day the event starts.")
    end_date = models.DateField(
        "Last day",
        null=True,
        blank=True,
        help_text="Only for events running more than one day, e.g. an Akhand Paath.",
    )
    start_time = models.TimeField(
        blank=True, null=True, help_text="Optional. Leave blank if it varies."
    )
    location = models.CharField(
        max_length=120, blank=True, default="Main Hall", help_text="Optional."
    )
    image = models.ImageField(
        "Poster",
        upload_to="events/",
        blank=True,
        help_text="Optional. A poster or photo for this event.",
    )
    description = models.TextField(
        blank=True, help_text="A short paragraph shown under the event title."
    )
    is_featured = models.BooleanField(
        "Highlight this event",
        default=False,
        help_text="Highlighted events stand out and are listed first.",
    )

    class Meta:
        ordering = ["date", "start_time"]
        verbose_name = "Event"
        verbose_name_plural = "Events & posters"

    def __str__(self):
        return f"{self.title} — {self.date:%b %d, %Y}"

    @property
    def is_past(self):
        return (self.end_date or self.date) < timezone.localdate()

    @classmethod
    def upcoming(cls):
        """Past events drop off the site automatically — nothing to clean up."""
        today = timezone.localdate()
        return cls.objects.filter(
            models.Q(end_date__gte=today) | models.Q(end_date__isnull=True, date__gte=today)
        ).order_by("-is_featured", "date")


class ProgramItem(models.Model):
    """A row of the daily programme, shown in the footer and on Livestream."""

    heading = models.CharField(
        max_length=120,
        help_text="For example 'Morning Program' or 'Wednesday & Friday'.",
    )
    days = models.CharField(
        max_length=120,
        blank=True,
        help_text="For example 'Daily' or '7 days a week'. Optional.",
    )
    items = models.TextField(
        "What happens",
        help_text="For example: Nitnem · Asa Di Vaar · Ardas · Hukamnama",
    )
    sort_order = models.PositiveIntegerField(
        "Order", default=0, help_text="Lower numbers show first."
    )
    is_highlighted = models.BooleanField(
        "Highlight this row",
        default=False,
        help_text="Use for programmes that only run on certain days.",
    )

    class Meta:
        ordering = ["sort_order", "id"]
        verbose_name = "Programme row"
        verbose_name_plural = "Daily programme"

    def __str__(self):
        return self.heading
