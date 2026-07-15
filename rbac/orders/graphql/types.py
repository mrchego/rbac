import strawberry
import strawberry_django
from strawberry import auto
from typing import List
from decimal import Decimal

from rbac.orders.models import Order, OrderLineItem


@strawberry_django.type(OrderLineItem)
class OrderLineItemType:
    id: auto
    description: auto
    quantity: auto
    unit_price: auto


@strawberry_django.type(Order)
class OrderType:
    id: auto
    reference: auto
    status: auto
    notes: auto
    created_at: auto
    updated_at: auto

    @strawberry.field
    def line_items(self) -> List[OrderLineItemType]:
        return list(self.line_items.all())

    @strawberry.field
    def total(self) -> Decimal:
        return self.total