# accounts/services/lock_user.py
from django.db import transaction
from django.utils import timezone
from rbac.accounts.selectors import get_user
from rbac.accounts.services.ownership_guard import assert_not_last_owner
from rbac.core.exceptions import ApplicationError, ErrorCode

@transaction.atomic
def lock_user(*, user_id, duration_minutes=15):
    user = get_user(user_id=user_id)
    if not user:
        raise ApplicationError("User not found.", code=ErrorCode.USER_NOT_FOUND)
    if user.company_id:
        assert_not_last_owner(user=user, company_id=str(user.company_id), action="locked")

    user.locked_until = timezone.now() + timezone.timedelta(minutes=duration_minutes)
    user.save(update_fields=['locked_until'])
    return user