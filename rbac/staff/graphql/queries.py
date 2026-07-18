import strawberry
from typing import List, Optional

from rbac.staff.graphql.types import InvitationType
from rbac.staff.selectors import (
    list_invitations,
    list_staff_members,
    count_pending_invitations,
)
from rbac.accounts.graphql.types import UserType
from rbac.accounts.selectors import get_current_user
from rbac.authorization.decorators import require_owner
from rbac.core.exceptions import AppPermissionDeniedError


@strawberry.type
class StaffQuery:
    @strawberry.field
    @require_owner()
    def invitations(
        self, info: strawberry.Info, used: Optional[bool] = None
    ) -> List[InvitationType]:
        current = get_current_user(info)
        if not current or not current.company_id:
            raise AppPermissionDeniedError("No company context.")
        return list(list_invitations(company_id=str(current.company_id), used=used))

    @strawberry.field
    @require_owner()
    def pending_invitations_count(self, info: strawberry.Info) -> int:
        current = get_current_user(info)
        if not current or not current.company_id:
            raise AppPermissionDeniedError("No company context.")
        return count_pending_invitations(company_id=str(current.company_id))

    @strawberry.field
    @require_owner()
    def staff_members(
        self, info: strawberry.Info, can_login: Optional[bool] = None
    ) -> List[UserType]:
        current = get_current_user(info)
        if not current or not current.company_id:
            raise AppPermissionDeniedError("No company context.")
        return list(
            list_staff_members(company_id=str(current.company_id), can_login=can_login)
        )
