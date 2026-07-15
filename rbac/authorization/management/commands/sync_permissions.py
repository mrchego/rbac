# rbac/rbac/management/commands/sync_permissions.py
from django.core.management.base import BaseCommand

from rbac.authorization.models.permission import Permission
from rbac.authorization.permissions import PERMISSION_REGISTRY


class Command(BaseCommand):
    help = "Syncs PERMISSION_REGISTRY into the database."

    def handle(self, *args, **options):
        codenames_in_code = {codename for codename, _, _ in PERMISSION_REGISTRY}

        for codename, label, category in PERMISSION_REGISTRY:
            Permission.objects.update_or_create(
                codename=codename,
                defaults={"label": label, "category": category},
            )

        stale = Permission.objects.exclude(codename__in=codenames_in_code)
        if stale.exists():
            self.stdout.write(
                self.style.WARNING(
                    f"{stale.count()} permission(s) in DB no longer in code: "
                    f"{list(stale.values_list('codename', flat=True))}"
                )
            )
        self.stdout.write(self.style.SUCCESS("Permissions synced."))
