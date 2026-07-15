from django.db import transaction
from rbac.authorization.models.permission import Permission
from rbac.authorization.models.role import Role
from rbac.core.exceptions import ApplicationError, AppValidationError, ErrorCode


@transaction.atomic
def update_role(*, role_id, name=None, permission_codenames=None, is_default=None):
    role = Role.objects.filter(pk=role_id).first()
    if not role:
        raise ApplicationError("Role not found.", code=ErrorCode.ROLE_NOT_FOUND)

    if name is not None:
        name = name.strip()
        if len(name) < 2:
            raise AppValidationError("Role name must be at least 2 characters long.", field="name")
        role.name = name

    if is_default is not None:
        role.is_default = is_default

    role.save()

    if permission_codenames is not None:
        permissions = list(Permission.objects.filter(codename__in=permission_codenames))
        role.permissions.set(permissions)

    return role