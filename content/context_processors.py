from .models import PageText, Photo, SiteSettings, Stat


def site_settings(request):
    """Makes the editable content available in every template.

    Views don't pass any of this, so adding a page never means remembering to
    wire up the gurdwara's name, its phone numbers or its wording again.

    `text` is keyed by block, so a template reads {{ text.home_about.heading }}.
    A missing row returns an empty block rather than blowing up, which keeps a
    half-seeded database from taking the site down.
    """
    blocks = {t.key: t for t in PageText.objects.all()}

    credits = (
        Photo.objects.filter(is_active=True)
        .exclude(credit="")
        .values_list("credit", flat=True)
        .distinct()
    )

    return {
        "site": SiteSettings.load(),
        "text": blocks,
        "stats": Stat.objects.filter(is_active=True),
        # Photos we don't own are used under licences that require attribution,
        # and the footer is where that gets paid.
        "photo_credits": list(credits),
    }
