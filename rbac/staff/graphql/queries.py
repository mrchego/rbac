import strawberry
from typing import List, Optional

from rbac.staff.graphql.types import InvitationType
from rbac.staff.selectors import list_invitations
from rbac.accounts.selectors import get_current_user
from rbac.authorization.decorators import require_owner
from rbac.core.exceptions import AppPermissionDeniedError


@strawberry.type
class StaffQuery:
    @strawberry.field
    @require_owner()
    def invitations(self, info: strawberry.Info, used: Optional[bool] = None) -> List[InvitationType]:
        current = get_current_user(info)
        if not current or not current.company_id:
            raise AppPermissionDeniedError("No company context.")
        return list(list_invitations(company_id=str(current.company_id), used=used))