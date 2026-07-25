from django.db import transaction

from rbac.accounts.selectors import get_users_by_ids
from rbac.authorization.models.user_role import UserRole
from rbac.authorization.selectors.get_role import get_role
from rbac.authorization.selectors.get_user_permissions import invalidate_user_permissions_cache
from rbac.core.services.bulk_result import BulkActionResult


@transaction.atomic
def bulk_remove_role(*, user_ids, role_id, company_id):
    result = BulkActionResult()

    role = get_role(role_id=role_id, company_id=company_id)
    if not role:
        result.add_failure("*", "Role not found.")
        return result

    user_ids = [str(uid) for uid in user_ids]
    users = list(get_users_by_ids(user_ids=user_ids, company_id=company_id))
    found_ids = {str(u.id) for u in users}

    for user in users:
        uid = str(user.id)
        deleted, _ = UserRole.objects.filter(user=user, role=role).delete()
        if deleted:
            invalidate_user_permissions_cache(user_id=user.id)
            result.add_success(uid)
        else:
            result.add_failure(uid, "Role was not assigned.")

    for missing in set(user_ids) - found_ids:
        result.add_failure(missing, "User not found in this company.")

    return result