import strawberry
from typing import Optional, List

from rbac.accounts.graphql.types import UserType
from rbac.core.graphql.errors import MutationError


@strawberry.type
class UserMutationPayload:
    success: bool
    user: Optional[UserType] = None
    errors: Optional[List[MutationError]] = None


