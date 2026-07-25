from typing import Optional

from rbac.accounts.models import User
from rbac.authorization.models import UserRole
from rbac.core.pagination import paginate_queryset


def list_staff_members(
    *,
    company_id: str,
    can_login: Optional[bool] = None,
    limit: Optional[int] = None,
    offset: int = 0,
):
    """Users in this company who have at least one role assigned —
    i.e. actual staff, not just any company user record."""
    staff_ids = UserRole.objects.filter(
        user__company_id=company_id
    ).values_list("user_id", flat=True)

    qs = User.objects.select_related("company").filter(id__in=staff_ids, company_id=company_id)
    if can_login is not None:
        qs = qs.filter(can_login=can_login)
    return paginate_queryset(qs.order_by("-created_at"), limit=limit, offset=offset)