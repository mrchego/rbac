from django.db import transaction
from rbac.accounts.selectors import get_user

@transaction.atomic
def unlock_user(*, user_id):
    user = get_user(user_id=user_id)
    user.locked_until = None
    user.failed_login_attempts = 0
    user.save(update_fields=['locked_until', 'failed_login_attempts'])
    return user