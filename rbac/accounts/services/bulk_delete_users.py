from django.db import transaction
from rbac.accounts.selectors import get_users_by_ids
from rbac.accounts.services.bulk_result import BulkActionResult


@transaction.atomic
def bulk_delete_users(*, user_ids, company_id, current_user_id):
    result = BulkActionResult()
    user_ids = [str(uid) for uid in user_ids]
    current_user_id = str(current_user_id)
    users = list(get_users_by_ids(user_ids=user_ids, company_id=company_id))
    found_ids = {str(u.id) for u in users}

    for user in users:
        uid = str(user.id)

        if uid == current_user_id:
            result.add_failure(uid, "You cannot delete your own account.")
            continue
        if user.is_superuser:
            result.add_failure(uid, "Owner accounts cannot be bulk-deleted.")
            continue
        if not user.is_active and not user.can_login:
            result.add_failure(uid, "Already deleted.")
            continue

        user.is_active = False
        user.can_login = False
        user.save(update_fields=["is_active", "can_login"])
        result.add_success(uid)

    for missing in set(user_ids) - found_ids:
        result.add_failure(missing, "User not found in this company.")

    return result