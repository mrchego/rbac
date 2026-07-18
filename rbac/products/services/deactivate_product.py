from django.db import transaction
from rbac.products.selectors import get_product
from rbac.core.exceptions import ApplicationError, ErrorCode


@transaction.atomic
def deactivate_product(*, product_id):
    product = get_product(product_id=product_id)
    if not product:
        raise ApplicationError("Product not found.", code=ErrorCode.VALIDATION_ERROR)
    product.is_active = False
    product.save(update_fields=["is_active"])
    return product