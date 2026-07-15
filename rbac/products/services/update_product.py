from django.db import transaction, IntegrityError
from rbac.products.models import Product
from rbac.core.exceptions import ApplicationError, AppValidationError, BusinessRuleViolationError, ErrorCode


@transaction.atomic
def update_product(*, product_id, name=None, sku=None, price=None, is_active=None):
    product = Product.objects.filter(pk=product_id).first()
    if not product:
        raise ApplicationError("Product not found.", code=ErrorCode.VALIDATION_ERROR)

    if name is not None:
        name = name.strip()
        if len(name) < 2:
            raise AppValidationError("Product name must be at least 2 characters long.", field="name")
        product.name = name
    if sku is not None:
        sku = sku.strip()
        if not sku:
            raise AppValidationError("SKU is required.", field="sku")
        product.sku = sku
    if price is not None:
        if price < 0:
            raise AppValidationError("Price cannot be negative.", field="price")
        product.price = price
    if is_active is not None:
        product.is_active = is_active

    try:
        product.save()
    except IntegrityError:
        raise BusinessRuleViolationError(
            "A product with this SKU already exists.", code=ErrorCode.BUSINESS_RULE
        )
    return product