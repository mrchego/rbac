from django.db import transaction
from rbac.products.models import Product
from rbac.core.exceptions import ApplicationError, ErrorCode


@transaction.atomic
def delete_product(*, product_id):
    product = Product.objects.filter(pk=product_id).first()
    if not product:
        raise ApplicationError("Product not found.", code=ErrorCode.VALIDATION_ERROR)
    product.delete()
    return True