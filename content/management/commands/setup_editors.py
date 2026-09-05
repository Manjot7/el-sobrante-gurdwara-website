from django.core.management.base import BaseCommand

from content.admin import EDITOR_GROUP_NAME, ensure_editor_group


class Command(BaseCommand):
    help = (
        "Create the 'Website editors' group, which can manage photos, events, "
        "the programme and gurdwara details — and nothing else."
    )

    def handle(self, *args, **options):
        group = ensure_editor_group()
        self.stdout.write(
            self.style.SUCCESS(
                f"'{EDITOR_GROUP_NAME}' ready with {group.permissions.count()} "
                "permissions."
            )
        )
        self.stdout.write(
            "To add a committee member: create a user in the Django shell or by "
            "an admin account, tick 'Staff status', and add them to this group."
        )
