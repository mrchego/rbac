from django.db import transaction

from rbac.authorization.models.user_role import UserRole
from rbac.authorization.selectors.get_user_permissions import invalidate_user_permissions_cache
from rbac.core.exceptions import ApplicationError, ErrorCode


@transaction.atomic
def remove_role(*, user_id, role_id, company_id):
    deleted, _ = UserRole.objects.filter(
        user_id=user_id,
        role_id=role_id,
        role__company_id=company_id,
    ).delete()
    if not deleted:
        raise ApplicationError("User does not have this role assigned.", code=ErrorCode.BUSINESS_RULE)

    invalidate_user_permissions_cache(user_id=user_id)
    return True