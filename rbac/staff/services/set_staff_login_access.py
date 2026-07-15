from django.db import transaction
from rbac.accounts.selectors import get_user
from rbac.core.exceptions import ApplicationError, ErrorCode


@transaction.atomic
def set_staff_login_access(*, user_id, can_login):
    user = get_user(user_id=user_id)
    if not user:
        raise ApplicationError("User not found.", code=ErrorCode.USER_NOT_FOUND)

    user.can_login = can_login
    # Enabling login access for a records-only staff member who was never
    # invited still needs a password before they can actually log in — that's
    # a separate "send them an invitation" step, not handled here.
    user.save(update_fields=["can_login"])
    return user