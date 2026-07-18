from typing import Optional
from rbac.accounts.models import User
from rbac.authorization.models import UserRole


def list_staff_members(*, company_id: str, can_login: Optional[bool] = None):
    """Users in this company who have at least one role assigned —
    i.e. actual staff, not just any company user record."""
    staff_ids = UserRole.objects.filter(
        user__company_id=company_id
    ).values_list("user_id", flat=True)

    qs = User.objects.filter(id__in=staff_ids, company_id=company_id)
    if can_login is not None:
        qs = qs.filter(can_login=can_login)
    return qs.order_by("-created_at")