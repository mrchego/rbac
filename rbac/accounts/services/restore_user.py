from django.db import transaction
from rbac.accounts.selectors import get_user
from rbac.core.exceptions import ApplicationError, ErrorCode


@transaction.atomic
def restore_user(*, user_id):
    """
    Undoes delete_user: restores both is_active and can_login. A plain
    activate_user() only flips is_active, so it can't bring back a user
    whose can_login was also switched off by delete_user() — this is the
    dedicated undo for that specific state.
    """
    user = get_user(user_id=user_id)
    if not user:
        raise ApplicationError("User not found.", code=ErrorCode.USER_NOT_FOUND)

    user.is_active = True
    user.can_login = True
    user.save(update_fields=["is_active", "can_login"])
    return user