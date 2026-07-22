from typing import Optional
from rbac.authorization.models import Permission


def get_permission(*, codename: str) -> Optional[Permission]:
    return Permission.objects.filter(codename=codename).first()


def list_permissions(*, category: Optional[str] = None):
    qs = Permission.objects.all()
    if category:
        qs = qs.filter(category=category)
    return qs.order_by("category", "codename")