from django.utils import timezone
from django.db import transaction
from django.core.exceptions import ValidationError

from rbac.accounts.validators import validate_password_strength
from rbac.core.exceptions import AppValidationError


def _set_new_password(user, new_password):
    try:
        validate_password_strength(new_password)
    except ValidationError as e:
        raise AppValidationError(e.message, field="new_password")

    user.set_password(new_password)
    user.last_password_change = timezone.now()
    user.failed_login_attempts = 0
    user.locked_until = None
    user.password_reset_required = False
    user.save(
        update_fields=[
            "password",
            "last_password_change",
            "failed_login_attempts",
            "locked_until",
            "password_reset_required",
        ]
    )


@transaction.atomic
def change_password(user, current_password, new_password):
    """Self-service password change — requires proving knowledge of the current password."""
    if not user.check_password(current_password):
        raise AppValidationError("Current password is incorrect.", field="current_password")
    _set_new_password(user, new_password)


@transaction.atomic
def set_password_unchecked(user, new_password):
    """
    For flows where the caller has already established authority another way
    (invitation token, email-verified reset link, admin force-reset) — no
    current password to check because there either isn't one yet or the
    proof of identity already happened elsewhere.
    """
    _set_new_password(user, new_password)