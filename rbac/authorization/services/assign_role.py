from django.db import transaction, IntegrityError
from rbac.accounts.selectors import get_user
from rbac.authorization.models.role import Role
from rbac.authorization.models.user_role import UserRole
from rbac.core.exceptions import ApplicationError, ErrorCode


@transaction.atomic
def assign_role(*, user_id, role_id):
    user = get_user(user_id=user_id)
    if not user:
        raise ApplicationError("User not found.", code=ErrorCode.USER_NOT_FOUND)

    role = Role.objects.filter(pk=role_id).first()
    if not role:
        raise ApplicationError("Role not found.", code=ErrorCode.ROLE_NOT_FOUND)

    if role.company_id != user.company_id:
        raise ApplicationError("Role does not belong to the user's company.", code=ErrorCode.PERMISSION_DENIED)

    try:
        UserRole.objects.create(user=user, role=role)
    except IntegrityError:
        pass  # already assigned — idempotent, not an error

    return True