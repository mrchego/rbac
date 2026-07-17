import strawberry
from typing import Optional, List

from rbac.accounts.graphql.types import UserType
from rbac.core.graphql.errors import MutationError


@strawberry.type
class UserMutationPayload:
    success: bool
    user: Optional[UserType] = None
    errors: Optional[List[MutationError]] = None
    
@strawberry.type
class BulkActionFailure:
    user_id: strawberry.ID
    reason: str


@strawberry.type
class BulkUserActionPayload:
    """success=True only if every row succeeded — but succeeded_ids/failed
    are always populated, so the frontend can show partial results either way."""
    success: bool
    succeeded_ids: List[strawberry.ID]
    failed: List[BulkActionFailure]


