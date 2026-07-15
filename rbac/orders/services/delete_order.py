from django.db import transaction
from rbac.orders.models import Order
from rbac.core.exceptions import ApplicationError, ErrorCode


@transaction.atomic
def delete_order(*, order_id):
    order = Order.objects.filter(pk=order_id).first()
    if not order:
        raise ApplicationError("Order not found.", code=ErrorCode.VALIDATION_ERROR)
    if order.status != Order.Status.DRAFT:
        raise ApplicationError(
            "Only draft orders can be deleted. Cancel it instead.", code=ErrorCode.BUSINESS_RULE
        )
    order.delete()
    return True