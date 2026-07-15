from django.db import transaction
from django.utils import timezone
from rbac.accounts.selectors import get_user

@transaction.atomic
def lock_user(*, user_id, duration_minutes=15):
    user = get_user(user_id=user_id)
    user.locked_until = timezone.now() + timezone.timedelta(minutes=duration_minutes)
    user.save(update_fields=['locked_until'])
    return user