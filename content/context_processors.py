from .models import Photo, SiteSettings


def site_settings(request):
    """Makes {{ site }} and {{ photo_credits }} available in every template.

    Views don't need to pass these, so adding a new page never means
    remembering to wire up the gurdwara's name and phone numbers again.

    photo_credits is not decoration: photos we don't own are used under
    licences that require attribution, and the footer is where that is paid.
    """
    credits = (
        Photo.objects.filter(is_active=True)
        .exclude(credit="")
        .values_list("credit", flat=True)
        .distinct()
    )
    return {
        "site": SiteSettings.load(),
        "photo_credits": list(credits),
    }
