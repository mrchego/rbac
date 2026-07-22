from typing import Optional
from rbac.authorization.models import Role


def get_role(*, role_id: str, company_id: Optional[str] = None) -> Optional[Role]:
    qs = Role.objects.filter(pk=role_id)
    if company_id:
        qs = qs.filter(company_id=company_id)
    return qs.first()