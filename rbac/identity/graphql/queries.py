import strawberry
from typing import Optional

from rbac.identity.graphql.types import SessionType
from rbac.identity.selectors import get_active_session
from rbac.accounts.selectors import get_current_user


@strawberry.type
class SessionQuery:
    @strawberry.field
    def session(self, info: strawberry.Info) -> Optional[SessionType]:
        user = get_current_user(info)
        if not user:
            return None
        data = get_active_session(user_id=str(user.id))
        return SessionType(
            user_id=data["user_id"], active=data["active"], created_at=data["created_at"]
        )