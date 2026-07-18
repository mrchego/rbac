from typing import Optional
from django.db.models import Q
from rbac.products.models import Product


def search_products(*, company_id: str, query: str, is_active: Optional[bool] = None):
    """Case-insensitive match against name or SKU, scoped to a company. Useful
    for admin search/autocomplete UIs."""
    qs = Product.objects.filter(company_id=company_id)
    if query:
        qs = qs.filter(Q(name__icontains=query) | Q(sku__icontains=query))
    if is_active is not None:
        qs = qs.filter(is_active=is_active)
    return qs.order_by("name")