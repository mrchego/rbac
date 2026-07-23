# accounts/services/promote_to_owner.py
from django.db import transaction
from rbac.accounts.selectors import get_user
from rbac.core.exceptions import ApplicationError, ErrorCode


@transaction.atomic
def promote_to_owner(*, user_id):
    user = get_user(user_id=user_id)
    if not user:
        raise ApplicationError("User not found.", code=ErrorCode.USER_NOT_FOUND)
    if user.is_superuser:
        raise ApplicationError("User is already an owner.", code=ErrorCode.VALIDATION_ERROR)

    user.is_superuser = True
    user.is_staff = True
    user.save(update_fields=["is_superuser", "is_staff"])
    return user