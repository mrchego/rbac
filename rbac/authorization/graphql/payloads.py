import strawberry
from typing import Optional, List
from rbac.authorization.graphql.types import RoleType
from rbac.core.graphql.errors import MutationError


@strawberry.type
class RoleMutationPayload:
    success: bool
    role: Optional[RoleType] = None
    errors: Optional[List[MutationError]] = None


@strawberry.type
class AssignmentMutationPayload:
    success: bool
    errors: Optional[List[MutationError]] = None