import strawberry
from typing import Optional, List

from rbac.accounts.graphql.types import UserType
from rbac.core.graphql.errors import MutationError
from rbac.core.graphql.payloads import BulkActionFailure, BulkActionPayload  # noqa: F401


@strawberry.type
class UserMutationPayload:
    success: bool
    user: Optional[UserType] = None
    errors: Optional[List[MutationError]] = None


# Kept as an alias so existing imports of BulkUserActionPayload keep working.
BulkUserActionPayload = BulkActionPayload