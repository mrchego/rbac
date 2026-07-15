import strawberry
from typing import List, Optional
from decimal import Decimal


@strawberry.input
class OrderLineItemInput:
    description: str
    quantity: int
    unit_price: Decimal


@strawberry.input
class CreateOrderInput:
    reference: str
    notes: str = ""
    line_items: List[OrderLineItemInput] = strawberry.field(default_factory=list)


@strawberry.input
class OrderIdInput:
    order_id: strawberry.ID