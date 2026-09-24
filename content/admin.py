"""
The admin the committee actually uses.

Design rules for anything added here:
  - Every field gets help_text written for someone who has never used a CMS.
  - Labels use the words the committee uses, not model/field names.
  - Nothing is ever deleted to hide it — that's what "Show on the website" is for.
  - Editors never see Users, Groups or Permissions.
"""

from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group, Permission, User
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import Event, PageText, Photo, ProgramItem, SiteSettings, Stat

admin.site.site_header = "Sikh Center of SF Bay Area"
admin.site.site_title = "Website admin"
admin.site.index_title = "What would you like to update?"


def _thumb(image, height=52):
    """Small preview so photos are recognised by sight, not by filename."""
    if not image:
        return mark_safe('<span style="color:#999">No photo</span>')
    return format_html(
        '<img src="{}" style="height:{}px;width:auto;border-radius:4px;'
        'object-fit:cover;box-shadow:0 1px 3px rgba(0,0,0,.25)">',
        image.url,
        height,
    )


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ("preview", "caption_or_blank", "category", "sort_order", "is_active")
    list_display_links = ("preview", "caption_or_blank")
    list_editable = ("sort_order", "is_active")
    list_filter = ("category", "is_active")
    ordering = ("category", "sort_order")
    readonly_fields = ("large_preview",)
    fields = ("image", "large_preview", "category", "caption", "sort_order", "is_active")
    save_on_top = True

    @admin.display(description="Photo")
    def preview(self, obj):
        return _thumb(obj.image)

    @admin.display(description="Preview")
    def large_preview(self, obj):
        return _thumb(obj.image, height=220)

    @admin.display(description="Caption")
    def caption_or_blank(self, obj):
        return obj.caption or "—"


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("preview", "title", "date", "end_date", "is_featured", "status")
    list_display_links = ("preview", "title")
    list_editable = ("is_featured",)
    list_filter = ("is_featured",)
    date_hierarchy = "date"
    ordering = ("-date",)
    readonly_fields = ("large_preview",)
    save_on_top = True
    fieldsets = (
        (None, {"fields": ("title", "description")}),
        ("When", {"fields": ("date", "end_date", "start_time", "location")}),
        ("Poster", {"fields": ("image", "large_preview")}),
        ("Options", {"fields": ("is_featured",)}),
    )

    @admin.display(description="Poster")
    def preview(self, obj):
        return _thumb(obj.image)

    @admin.display(description="Preview")
    def large_preview(self, obj):
        return _thumb(obj.image, height=220)

    @admin.display(description="On the website?")
    def status(self, obj):
        if obj.is_past:
            return mark_safe(
                '<span style="color:#999">Finished — hidden automatically</span>'
            )
        return mark_safe('<span style="color:#137333">Showing</span>')


@admin.register(ProgramItem)
class ProgramItemAdmin(admin.ModelAdmin):
    list_display = ("heading", "days", "items", "sort_order", "is_highlighted")
    list_editable = ("sort_order", "is_highlighted")
    ordering = ("sort_order",)
    save_on_top = True


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    save_on_top = True
    fieldsets = (
        ("Name", {"fields": ("name", "gurmukhi_name", "location_line")}),
        (
            "Contact details",
            {
                "fields": (
                    "address_line1",
                    "address_line2",
                    "phone_main",
                    "phone_alt",
                    "email",
                    "opening_hours",
                )
            },
        ),
        (
            "YouTube",
            {
                "fields": ("youtube_channel_id", "youtube_channel_url", "facebook_url"),
                "description": (
                    "The livestream page follows the channel, so it plays whatever "
                    "is live at the time. There is nothing to change when a new "
                    "stream starts."
                ),
            },
        ),
        (
            "Calendar",
            {
                "fields": (
                    "google_calendar_id",
                    "nanakshahi_calendar_id",
                    "booking_note",
                ),
                "description": (
                    "Paths and bookings are entered in Google Calendar, not here. "
                    "Visitors can see the calendar but cannot change it."
                ),
            },
        ),
    )

    def has_add_permission(self, request):
        # There is only ever one row, so hide "Add" entirely.
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        """Skip the one-row list and open the edit form directly."""
        from django.shortcuts import redirect

        settings_obj = SiteSettings.load()
        return redirect(
            reverse("admin:content_sitesettings_change", args=[settings_obj.pk])
        )


@admin.register(PageText)
class PageTextAdmin(admin.ModelAdmin):
    """Fixed set of rows — editors reword them, they never add or remove one."""

    list_display = ("__str__", "heading", "preview")
    fields = ("heading", "body")
    ordering = ("sort_order",)
    save_on_top = True

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    @admin.display(description="Text")
    def preview(self, obj):
        text = " ".join(obj.body.split())
        return (text[:90] + "…") if len(text) > 90 else (text or "—")


@admin.register(Stat)
class StatAdmin(admin.ModelAdmin):
    list_display = ("value", "label", "sort_order", "is_active")
    list_editable = ("sort_order", "is_active")
    ordering = ("sort_order",)
    save_on_top = True


# Account management belongs to whoever owns the site, not to editors — but
# hiding it from everyone meant nobody could add a committee login without a
# developer, which defeats the point of handing the site over. So: visible to
# superusers, invisible to editors.
class _SuperuserOnlyMixin:
    def has_module_permission(self, request):
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(User)
class RestrictedUserAdmin(_SuperuserOnlyMixin, UserAdmin):
    pass


@admin.register(Group)
class RestrictedGroupAdmin(_SuperuserOnlyMixin, GroupAdmin):
    pass


EDITOR_GROUP_NAME = "Website editors"


def ensure_editor_group():
    """Create the editor group with content permissions only.

    Called from the `setup_editors` management command rather than at import
    time, so it never runs against an unmigrated database.
    """
    group, _ = Group.objects.get_or_create(name=EDITOR_GROUP_NAME)
    perms = Permission.objects.filter(
        content_type__app_label="content",
        codename__in=[
            "add_photo", "change_photo", "delete_photo", "view_photo",
            "add_event", "change_event", "delete_event", "view_event",
            "add_programitem", "change_programitem", "delete_programitem",
            "view_programitem",
            "add_stat", "change_stat", "delete_stat", "view_stat",
            # Singletons and fixed rows: editable, never added or deleted.
            "change_sitesettings", "view_sitesettings",
            "change_pagetext", "view_pagetext",
        ],
    )
    group.permissions.set(perms)
    return group
