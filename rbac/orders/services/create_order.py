from django.db import transaction, IntegrityError
from rbac.orders.models import Order, OrderLineItem
from rbac.core.exceptions import AppValidationError, BusinessRuleViolationError, ErrorCode


@transaction.atomic
def create_order(*, company, created_by, reference, notes="", line_items=None):
    reference = reference.strip()
    if not reference:
        raise AppValidationError("Reference is required.", field="reference")

    try:
        order = Order.objects.create(
            company=company, created_by=created_by, reference=reference, notes=notes
        )
    except IntegrityError:
        raise BusinessRuleViolationError(
            "An order with this reference already exists.", code=ErrorCode.BUSINESS_RULE
        )

    for item in (line_items or []):
        if item["quantity"] <= 0:
            raise AppValidationError("Line item quantity must be positive.", field="quantity")
        if item["unit_price"] < 0:
            raise AppValidationError("Line item price cannot be negative.", field="unit_price")
        OrderLineItem.objects.create(
            order=order,
            description=item["description"],
            quantity=item["quantity"],
            unit_price=item["unit_price"],
        )

    return order