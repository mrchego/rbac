from typing import Optional
from rbac.orders.models import Order


def list_orders(*, company_id: str, status: Optional[str] = None):
    qs = Order.objects.filter(company_id=company_id)
    if status is not None:
        qs = qs.filter(status=status)
    return qs.order_by("-created_at")