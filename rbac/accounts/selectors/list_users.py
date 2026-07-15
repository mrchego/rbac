from typing import Optional
from rbac.accounts.models import User

# rbac/accounts/selectors/list_users.py
def list_users(*, company_id: Optional[str] = None, is_active: Optional[bool] = None):
    qs = User.objects.all()
    if company_id:
        qs = qs.filter(company_id=company_id)
    if is_active is not None:
        qs = qs.filter(is_active=is_active)
    return qs.order_by('-created_at')