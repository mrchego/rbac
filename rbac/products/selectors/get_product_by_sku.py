from typing import Optional
from rbac.products.models import Product


def get_product_by_sku(*, sku: str, company_id: str) -> Optional[Product]:
    """SKUs are unique per company (see unique_product_sku_per_company), so
    company_id is required here — unlike get_user_by_email, which is global."""
    return Product.objects.filter(sku=sku, company_id=company_id).first()