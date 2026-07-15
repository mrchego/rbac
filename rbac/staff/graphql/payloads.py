import strawberry
from typing import Optional, List

from rbac.staff.graphql.types import InvitationType
from rbac.accounts.graphql.types import UserType
from rbac.core.graphql.errors import MutationError


@strawberry.type
class InvitationMutationPayload:
    success: bool
    invitation: Optional[InvitationType] = None
    errors: Optional[List[MutationError]] = None


@strawberry.type
class AcceptInvitationPayload:
    success: bool
    user: Optional[UserType] = None
    errors: Optional[List[MutationError]] = None


