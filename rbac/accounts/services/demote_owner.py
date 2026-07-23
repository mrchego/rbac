# accounts/services/demote_owner.py
from django.db import transaction
from rbac.accounts.selectors import get_user
from rbac.accounts.services.ownership_guard import assert_not_last_owner
from rbac.core.exceptions import ApplicationError, ErrorCode


@transaction.atomic
def demote_owner(*, user_id, company_id):
    user = get_user(user_id=user_id)
    if not user:
        raise ApplicationError("User not found.", code=ErrorCode.USER_NOT_FOUND)
    if not user.is_superuser:
        raise ApplicationError("User is not an owner.", code=ErrorCode.VALIDATION_ERROR)

    # Founder check + last-owner check both live here, same as every other path.
    assert_not_last_owner(user=user, company_id=company_id, action="demoted")

    user.is_superuser = False
    user.save(update_fields=["is_superuser"])
    return user