from django.db import transaction, IntegrityError
from rbac.products.models import Product
from rbac.core.exceptions import AppValidationError, BusinessRuleViolationError, ErrorCode


@transaction.atomic
def create_product(*, company, name, sku, price, is_active=True):
    name = name.strip()
    sku = sku.strip()
    if len(name) < 2:
        raise AppValidationError("Product name must be at least 2 characters long.", field="name")
    if not sku:
        raise AppValidationError("SKU is required.", field="sku")
    if price < 0:
        raise AppValidationError("Price cannot be negative.", field="price")

    try:
        return Product.objects.create(
            company=company, name=name, sku=sku, price=price, is_active=is_active
        )
    except IntegrityError:
        raise BusinessRuleViolationError(
            "A product with this SKU already exists.", code=ErrorCode.BUSINESS_RULE
        )