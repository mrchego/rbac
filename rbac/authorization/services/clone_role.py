from django.db import transaction
from rbac.authorization.models.role import Role
from rbac.core.exceptions import ApplicationError, ErrorCode


@transaction.atomic
def clone_role(*, role_id, company_id, new_name):
    source = Role.objects.filter(pk=role_id, company_id=company_id).first()
    if not source:
        raise ApplicationError("Role not found.", code=ErrorCode.ROLE_NOT_FOUND)

    new_name = new_name.strip()
    if len(new_name) < 2:
        raise ApplicationError("Role name must be at least 2 characters long.", code=ErrorCode.VALIDATION_ERROR)

    clone = Role.objects.create(company_id=company_id, name=new_name, is_default=False)
    clone.permissions.set(source.permissions.all())
    return clone