from typing import Optional
from rbac.products.models import Product


def get_product(*, product_id: str) -> Optional[Product]:
    return Product.objects.filter(pk=product_id).first()