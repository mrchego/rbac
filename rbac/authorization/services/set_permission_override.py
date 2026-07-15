from django.db import transaction
from rbac.authorization.models.permission import Permission

from rbac.accounts.selectors import get_user
from rbac.authorization.models.user_role import UserPermissionOverride
from rbac.core.exceptions import ApplicationError, ErrorCode


@transaction.atomic
def set_permission_override(*, user_id, permission_codename, is_granted):
    user = get_user(user_id=user_id)
    if not user:
        raise ApplicationError("User not found.", code=ErrorCode.USER_NOT_FOUND)

    permission = Permission.objects.filter(codename=permission_codename).first()
    if not permission:
        raise ApplicationError("Permission not found.", code=ErrorCode.VALIDATION_ERROR)

    UserPermissionOverride.objects.update_or_create(
        user=user, permission=permission, defaults={"is_granted": is_granted}
    )
    return True


@transaction.atomic
def clear_permission_override(*, user_id, permission_codename):
    UserPermissionOverride.objects.filter(
        user_id=user_id, permission__codename=permission_codename
    ).delete()
    return True
