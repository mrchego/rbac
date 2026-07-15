from django.db import transaction
from rbac.accounts.selectors import get_user

@transaction.atomic
def delete_user(*, user_id):
    # Soft-delete by disabling the account and removing login ability.
    user = get_user(user_id=user_id)
    user.is_active = False
    user.can_login = False
    user.save(update_fields=['is_active', 'can_login'])
    return user