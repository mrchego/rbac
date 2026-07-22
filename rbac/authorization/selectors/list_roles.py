from rbac.authorization.models import Role


def list_roles(*, company_id: str):
    return Role.objects.filter(company_id=company_id).prefetch_related("permissions")