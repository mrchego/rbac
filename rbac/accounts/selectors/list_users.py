from typing import Optional
from rbac.accounts.models import User


# rbac/accounts/selectors/list_users.py
# rbac/accounts/selectors/list_user.py
def list_users(*, company_id=None, is_active=None, can_login=None):
    qs = User.objects.all()
    if company_id:
        qs = qs.filter(company_id=company_id)
    if is_active is not None:
        qs = qs.filter(is_active=is_active)
    if can_login is not None:
        qs = qs.filter(can_login=can_login)
    return qs.order_by("-created_at")
