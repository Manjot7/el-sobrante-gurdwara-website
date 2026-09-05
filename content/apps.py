from django.apps import AppConfig


class ContentConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "content"
    # Shown as the section heading on the admin home page.
    verbose_name = "Website content"
