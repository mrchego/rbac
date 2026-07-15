from django.db import transaction
from rbac.authorization.models.role import Role
from rbac.core.exceptions import ApplicationError, ErrorCode


@transaction.atomic
def delete_role(*, role_id):
    role = Role.objects.filter(pk=role_id).first()
    if not role:
        raise ApplicationError("Role not found.", code=ErrorCode.ROLE_NOT_FOUND)

    if role.user_roles.exists():
        raise ApplicationError(
            "Cannot delete a role that is still assigned to staff. Reassign them first.",
            code=ErrorCode.BUSINESS_RULE,
        )

    role.delete()
    return True