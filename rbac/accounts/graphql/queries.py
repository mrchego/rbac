import strawberry
from typing import List, Optional

from rbac.accounts.graphql.types import UserType
from rbac.accounts.selectors import get_current_user, get_user, list_users
from rbac.authorization.decorators import require_owner
from rbac.core.exceptions import AppPermissionDeniedError


@strawberry.type
class UserQuery:
    @strawberry.field
    def me(self, info: strawberry.Info) -> Optional[UserType]:
        return get_current_user(info)

    @strawberry.field
    @require_owner()
    def user(self, info: strawberry.Info , user_id: strawberry.ID) -> Optional[UserType]:
        return get_user(user_id=user_id)

    @strawberry.field
    @require_owner()
    def users(self, info: strawberry.Info, is_active: Optional[bool] = None) -> List[UserType]:
        current = get_current_user(info)
        if not current or not current.company_id:
            raise AppPermissionDeniedError("No company context.")
        return list(list_users(company_id=str(current.company_id), is_active=is_active))