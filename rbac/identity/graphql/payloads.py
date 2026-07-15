import strawberry
from typing import Optional, List

from rbac.identity.graphql.types import UserType, SessionType
from rbac.core.graphql.errors import MutationError


@strawberry.type
class AuthMutationPayload:
    success: bool
    user: Optional[UserType] = None
    errors: Optional[List[MutationError]] = None

