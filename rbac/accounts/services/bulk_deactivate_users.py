# accounts/services/bulk_deactivate_users.py
from django.db import transaction
from rbac.accounts.selectors import get_users_by_ids
from rbac.accounts.services.bulk_result import BulkActionResult
from rbac.accounts.services.ownership_guard import assert_not_last_owner
from rbac.core.exceptions import ApplicationError


@transaction.atomic
def bulk_deactivate_users(*, user_ids, company_id, current_user_id):
    result = BulkActionResult()
    user_ids = [str(uid) for uid in user_ids]
    current_user_id = str(current_user_id)
    users = list(get_users_by_ids(user_ids=user_ids, company_id=company_id))
    found_ids = {str(u.id) for u in users}

    for user in users:
        uid = str(user.id)

        if uid == current_user_id:
            result.add_failure(uid, "You cannot deactivate your own account.")
            continue
        if not user.is_active:
            result.add_failure(uid, "Already inactive.")
            continue

        try:
            assert_not_last_owner(user=user, company_id=company_id, action="deactivated")
        except ApplicationError as e:
            result.add_failure(uid, e.message)
            continue

        user.is_active = False
        user.save(update_fields=["is_active"])
        result.add_success(uid)

    for missing in set(user_ids) - found_ids:
        result.add_failure(missing, "User not found in this company.")

    return result