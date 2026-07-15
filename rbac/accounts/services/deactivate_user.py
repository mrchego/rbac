from django.db import transaction
from rbac.accounts.selectors import get_user

@transaction.atomic
def deactivate_user(*, user_id):
    user = get_user(user_id=user_id)
    user.is_active = False
    user.save(update_fields=['is_active'])
    return user