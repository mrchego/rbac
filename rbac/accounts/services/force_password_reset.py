from django.db import transaction
from rbac.accounts.selectors import get_user

@transaction.atomic
def force_password_reset(*, user_id):
    user = get_user(user_id=user_id)
    user.password_reset_required = True
    user.save(update_fields=['password_reset_required'])
    return user