from django.db import transaction
from rbac.accounts.selectors import get_users_by_ids, count_active_superusers
from rbac.accounts.services.bulk_result import BulkActionResult


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
        if user.is_superuser:
            # Checked per-row, after prior saves in this loop — so deactivating
            # three owners allows the first two and blocks only the one that
            # would leave the company with zero active owners.
            remaining = count_active_superusers(company_id=company_id, exclude_ids=[uid])
            if remaining == 0:
                result.add_failure(uid, "Cannot deactivate the last active owner of the company.")
                continue

        user.is_active = False
        user.save(update_fields=["is_active"])
        result.add_success(uid)

    for missing in set(user_ids) - found_ids:
        result.add_failure(missing, "User not found in this company.")

    return result