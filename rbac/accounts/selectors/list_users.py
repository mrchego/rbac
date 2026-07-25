from typing import Optional

from django.db.models import Q

from rbac.accounts.models import User
from rbac.core.pagination import paginate_queryset


def list_users(
    *,
    company_id=None,
    is_active: Optional[bool] = None,
    can_login: Optional[bool] = None,
    search: Optional[str] = None,
    limit: Optional[int] = None,
    offset: int = 0,
):
    """Returns (items, total_count). select_related("company") avoids an
    N+1 on UserType.company for every row returned in the page."""
    qs = User.objects.select_related("company").all()
    if company_id:
        qs = qs.filter(company_id=company_id)
    if is_active is not None:
        qs = qs.filter(is_active=is_active)
    if can_login is not None:
        qs = qs.filter(can_login=can_login)
    if search:
        qs = qs.filter(
            Q(email__icontains=search)
            | Q(first_name__icontains=search)
            | Q(last_name__icontains=search)
        )
    return paginate_queryset(qs.order_by("-created_at"), limit=limit, offset=offset)