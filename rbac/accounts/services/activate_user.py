from django.db import transaction
from rbac.accounts.selectors import get_user

@transaction.atomic
def activate_user(*, user_id):
    user = get_user(user_id=user_id)
    user.is_active = True
    user.save(update_fields=['is_active'])
    return user