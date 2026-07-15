from typing import Optional
from rbac.products.models import Product


def list_products(*, company_id: str, is_active: Optional[bool] = None):
    qs = Product.objects.filter(company_id=company_id)
    if is_active is not None:
        qs = qs.filter(is_active=is_active)
    return qs.order_by("name")