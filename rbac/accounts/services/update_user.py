from django.db import transaction
from rbac.accounts.selectors import get_user
from rbac.core.exceptions import ApplicationError, ErrorCode

@transaction.atomic
def update_user(*, user_id, **kwargs):
    user = get_user(user_id=user_id)
    if not user:
        raise ApplicationError("User not found.", code=ErrorCode.USER_NOT_FOUND)

    allowed_fields = ["first_name", "last_name", "phone", "avatar", "company"]
    for field in allowed_fields:
        if field in kwargs:
            setattr(user, field, kwargs[field])

    # If email is being updated, handle it separately because it has unique constraints
    if 'email' in kwargs:
        user.email = kwargs['email']

    user.full_clean()  # Validate the new data
    user.save()
    return user