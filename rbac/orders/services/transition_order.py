from django.db import transaction
from rbac.orders.models import Order
from rbac.core.exceptions import ApplicationError, BusinessRuleViolationError, ErrorCode

# Explicit allow-list of legal transitions. Anything not listed here is refused.
ALLOWED_TRANSITIONS = {
    Order.Status.DRAFT: {Order.Status.SUBMITTED, Order.Status.CANCELLED},
    Order.Status.SUBMITTED: {Order.Status.APPROVED, Order.Status.CANCELLED},
    Order.Status.APPROVED: {Order.Status.COMPLETED, Order.Status.CANCELLED},
    Order.Status.COMPLETED: set(),   # terminal
    Order.Status.CANCELLED: set(),   # terminal
}


@transaction.atomic
def transition_order(*, order_id, new_status):
    order = Order.objects.filter(pk=order_id).first()
    if not order:
        raise ApplicationError("Order not found.", code=ErrorCode.VALIDATION_ERROR)

    if new_status not in ALLOWED_TRANSITIONS.get(order.status, set()):
        raise BusinessRuleViolationError(
            f"Cannot move an order from {order.status} to {new_status}.",
            code=ErrorCode.BUSINESS_RULE,
        )

    order.status = new_status
    order.save(update_fields=["status"])
    return order