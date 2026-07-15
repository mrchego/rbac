import strawberry
from typing import Optional, List

from rbac.orders.graphql.types import OrderType
from rbac.core.graphql.errors import MutationError


@strawberry.type
class OrderMutationPayload:
    success: bool
    order: Optional[OrderType] = None
    errors: Optional[List[MutationError]] = None

