from typing import Optional, Iterable
from rbac.accounts.models import User


def count_active_superusers(*, company_id: str, exclude_ids: Optional[Iterable[str]] = None) -> int:
    """
    How many active superusers a company would have left if `exclude_ids`
    were removed from the count — used to check "is this the last owner?"
    without actually performing the removal first.
    """
    qs = User.objects.filter(company_id=company_id, is_superuser=True, is_active=True)
    if exclude_ids:
        qs = qs.exclude(pk__in=exclude_ids)
    return qs.count()