from typing import Optional

from rbac.core.pagination import paginate_queryset
from rbac.products.models import Product


def list_products(
    *,
    company_id: str,
    is_active: Optional[bool] = None,
    search: Optional[str] = None,
    limit: Optional[int] = None,
    offset: int = 0,
):
    qs = Product.objects.filter(company_id=company_id)
    if is_active is not None:
        qs = qs.filter(is_active=is_active)
    if search:
        from django.db.models import Q

        qs = qs.filter(Q(name__icontains=search) | Q(sku__icontains=search))
    return paginate_queryset(qs.order_by("name"), limit=limit, offset=offset)