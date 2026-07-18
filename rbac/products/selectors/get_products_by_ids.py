from typing import Optional
from rbac.products.models import Product


def get_products_by_ids(*, product_ids, company_id: Optional[str] = None):
    """Returns the subset of product_ids that actually exist (optionally scoped to a company)."""
    qs = Product.objects.filter(pk__in=product_ids)
    if company_id:
        qs = qs.filter(company_id=company_id)
    return qs