from typing import Optional
from rbac.staff.models import Invitation


def list_invitations(*, company_id: str, used: Optional[bool] = None):
    qs = Invitation.objects.filter(company_id=company_id)
    if used is not None:
        qs = qs.filter(used=used)
    return qs.order_by("-created_at")