from django.db import transaction
from rbac.accounts.selectors import get_users_by_ids
from rbac.accounts.services.bulk_result import BulkActionResult


@transaction.atomic
def bulk_force_password_reset(*, user_ids, company_id):
    result = BulkActionResult()
    user_ids = [str(uid) for uid in user_ids]
    users = list(get_users_by_ids(user_ids=user_ids, company_id=company_id))
    found_ids = {str(u.id) for u in users}

    for user in users:
        uid = str(user.id)
        user.password_reset_required = True
        user.save(update_fields=["password_reset_required"])
        result.add_success(uid)

    for missing in set(user_ids) - found_ids:
        result.add_failure(missing, "User not found in this company.")

    return result