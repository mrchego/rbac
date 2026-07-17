from typing import Optional
from rbac.accounts.models import User


def get_users_by_ids(*, user_ids, company_id: Optional[str] = None):
    """Returns the subset of user_ids that actually exist (optionally scoped to a company)."""
    qs = User.objects.filter(pk__in=user_ids)
    if company_id:
        qs = qs.filter(company_id=company_id)
    return qs