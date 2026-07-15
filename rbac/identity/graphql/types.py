import strawberry
from typing import Optional

from rbac.accounts.graphql.types import UserType  # re-exported for identity payloads


@strawberry.type
class SessionType:
    user_id: strawberry.ID
    active: bool
    created_at: Optional[str] = None