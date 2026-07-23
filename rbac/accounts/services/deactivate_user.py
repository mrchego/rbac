# accounts/services/deactivate_user.py
from django.db import transaction
from rbac.accounts.selectors import get_user
from rbac.accounts.services.ownership_guard import assert_not_last_owner
from rbac.core.exceptions import ApplicationError, ErrorCode

@transaction.atomic
def deactivate_user(*, user_id):
    user = get_user(user_id=user_id)
    if not user:
        raise ApplicationError("User not found.", code=ErrorCode.USER_NOT_FOUND)
    if user.company_id:
        assert_not_last_owner(user=user, company_id=str(user.company_id), action="deactivated")

    user.is_active = False
    user.save(update_fields=['is_active'])
    return user