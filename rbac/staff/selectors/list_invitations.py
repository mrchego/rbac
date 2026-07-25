from typing import Optional

from rbac.core.pagination import paginate_queryset
from rbac.staff.models import Invitation


def list_invitations(
    *,
    company_id: str,
    used: Optional[bool] = None,
    limit: Optional[int] = None,
    offset: int = 0,
):
    # select_related avoids a query-per-row for InvitationType.role_name
    # and InvitationType.invited_by_email when listing many invitations.
    qs = Invitation.objects.select_related("role", "invited_by").filter(company_id=company_id)
    if used is not None:
        qs = qs.filter(used=used)
    return paginate_queryset(qs.order_by("-created_at"), limit=limit, offset=offset)