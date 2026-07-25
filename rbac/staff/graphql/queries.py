from typing import Optional

import strawberry

from rbac.accounts.selectors import get_current_user
from rbac.authorization.decorators import require_owner
from rbac.core.exceptions import AppPermissionDeniedError
from rbac.staff.graphql.types import InvitationConnection, StaffMemberConnection
from rbac.staff.selectors import (
    count_pending_invitations,
    list_invitations,
    list_staff_members,
)


@strawberry.type
class StaffQuery:
    @strawberry.field
    @require_owner()
    def invitations(
        self,
        info: strawberry.Info,
        used: Optional[bool] = None,
        limit: Optional[int] = None,
        offset: int = 0,
    ) -> InvitationConnection:
        current = get_current_user(info)
        if not current or not current.company_id:
            raise AppPermissionDeniedError("No company context.")
        items, total_count = list_invitations(
            company_id=str(current.company_id), used=used, limit=limit, offset=offset
        )
        return InvitationConnection(items=items, total_count=total_count)

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
        self,
        info: strawberry.Info,
        can_login: Optional[bool] = None,
        limit: Optional[int] = None,
        offset: int = 0,
    ) -> StaffMemberConnection:
        current = get_current_user(info)
        if not current or not current.company_id:
            raise AppPermissionDeniedError("No company context.")
        items, total_count = list_staff_members(
            company_id=str(current.company_id), can_login=can_login, limit=limit, offset=offset
        )
        return StaffMemberConnection(items=items, total_count=total_count)