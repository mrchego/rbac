from typing import Optional
from rbac.orders.models import Order


def get_order(*, order_id: str) -> Optional[Order]:
    return Order.objects.filter(pk=order_id).first()