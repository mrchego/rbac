from typing import Optional

import strawberry

from rbac.accounts.selectors import get_current_user
from rbac.authorization.decorators import require_permission
from rbac.core.exceptions import AppPermissionDeniedError
from rbac.products.graphql.types import ProductConnection, ProductType
from rbac.products.selectors import get_product, list_products


@strawberry.type
class ProductQuery:
    @strawberry.field
    @require_permission("products.view_product")
    def product(self, info: strawberry.Info, product_id: strawberry.ID) -> Optional[ProductType]:
        return get_product(product_id=product_id)

    @strawberry.field
    @require_permission("products.view_product")
    def products(
        self,
        info: strawberry.Info,
        is_active: Optional[bool] = None,
        search: Optional[str] = None,
        limit: Optional[int] = None,
        offset: int = 0,
    ) -> ProductConnection:
        current = get_current_user(info)
        if not current or not current.company_id:
            raise AppPermissionDeniedError("No company context.")
        items, total_count = list_products(
            company_id=str(current.company_id),
            is_active=is_active,
            search=search,
            limit=limit,
            offset=offset,
        )
        return ProductConnection(items=items, total_count=total_count)