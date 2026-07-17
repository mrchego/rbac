from django.db import transaction
from rbac.accounts.selectors import get_users_by_ids
from rbac.accounts.services.bulk_result import BulkActionResult


@transaction.atomic
def bulk_unlock_users(*, user_ids, company_id):
    result = BulkActionResult()
    user_ids = [str(uid) for uid in user_ids]
    users = list(get_users_by_ids(user_ids=user_ids, company_id=company_id))
    found_ids = {str(u.id) for u in users}

    for user in users:
        uid = str(user.id)
        user.locked_until = None
        user.failed_login_attempts = 0
        user.save(update_fields=["locked_until", "failed_login_attempts"])
        result.add_success(uid)

    for missing in set(user_ids) - found_ids:
        result.add_failure(missing, "User not found in this company.")

    return result