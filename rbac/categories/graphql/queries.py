import strawberry
from typing import List, Optional

from rbac.categories.graphql.types import CategoryType
from rbac.categories.selectors import get_category, list_categories
from rbac.accounts.selectors import get_current_user
from rbac.authorization.decorators import require_permission
from rbac.core.exceptions import AppPermissionDeniedError


@strawberry.type
class CategoryQuery:
    @strawberry.field
    @require_permission("categories.view_category")
    def category(self, info: strawberry.Info, category_id: strawberry.ID) -> Optional[CategoryType]:
        return get_category(category_id=category_id)

    @strawberry.field
    @require_permission("categories.view_category")
    def categories(self, info: strawberry.Info, root_only: bool = False) -> List[CategoryType]:
        current = get_current_user(info)
        if not current or not current.company_id:
            raise AppPermissionDeniedError("No company context.")
        return list(list_categories(company_id=str(current.company_id), root_only=root_only))