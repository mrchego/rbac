from django.db import transaction, IntegrityError
from rbac.authorization.models.permission import Permission
from rbac.authorization.models.role import Role
from rbac.core.exceptions import AppValidationError, BusinessRuleViolationError, ErrorCode


@transaction.atomic
def create_role(*, company, name, permission_codenames=None, is_default=False):
    name = name.strip()
    if len(name) < 2:
        raise AppValidationError("Role name must be at least 2 characters long.", field="name")

    permissions = list(Permission.objects.filter(codename__in=permission_codenames or []))

    try:
        role = Role.objects.create(company=company, name=name, is_default=is_default)
        if permissions:
            role.permissions.set(permissions)
        return role
    except IntegrityError:
        raise BusinessRuleViolationError(
            "A role with this name already exists for this company.",
            code=ErrorCode.BUSINESS_RULE,
        )