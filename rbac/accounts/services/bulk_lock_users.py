# accounts/services/bulk_lock_users.py
from django.db import transaction
from django.utils import timezone
from rbac.accounts.selectors import get_users_by_ids
from rbac.accounts.services.bulk_result import BulkActionResult
from rbac.accounts.services.ownership_guard import assert_not_last_owner
from rbac.core.exceptions import ApplicationError


@transaction.atomic
def bulk_lock_users(*, user_ids, company_id, current_user_id, duration_minutes=15):
    result = BulkActionResult()
    user_ids = [str(uid) for uid in user_ids]
    current_user_id = str(current_user_id)
    users = list(get_users_by_ids(user_ids=user_ids, company_id=company_id))
    found_ids = {str(u.id) for u in users}
    locked_until = timezone.now() + timezone.timedelta(minutes=duration_minutes)

    for user in users:
        uid = str(user.id)
        if uid == current_user_id:
            result.add_failure(uid, "You cannot lock your own account.")
            continue

        try:
            assert_not_last_owner(user=user, company_id=company_id, action="locked")
        except ApplicationError as e:
            result.add_failure(uid, e.message)
            continue

        user.locked_until = locked_until
        user.save(update_fields=["locked_until"])
        result.add_success(uid)

    for missing in set(user_ids) - found_ids:
        result.add_failure(missing, "User not found in this company.")

    return result