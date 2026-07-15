import strawberry
from typing import List, Optional

from rbac.orders.graphql.types import OrderType
from rbac.orders.selectors import get_order, list_orders
from rbac.accounts.selectors import get_current_user
from rbac.authorization.decorators import require_permission
from rbac.core.exceptions import AppPermissionDeniedError


@strawberry.type
class OrderQuery:
    @strawberry.field
    @require_permission("orders.view_order")
    def order(self, info: strawberry.Info, order_id: strawberry.ID) -> Optional[OrderType]:
        return get_order(order_id=order_id)

    @strawberry.field
    @require_permission("orders.view_order")
    def orders(self, info: strawberry.Info, status: Optional[str] = None) -> List[OrderType]:
        current = get_current_user(info)
        if not current or not current.company_id:
            raise AppPermissionDeniedError("No company context.")
        return list(list_orders(company_id=str(current.company_id), status=status))