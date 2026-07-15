import strawberry
from typing import Optional


@strawberry.input
class InviteStaffInput:
    email: str
    first_name: str
    last_name: str
    can_login: bool = True
    role_id: Optional[strawberry.ID] = None


@strawberry.input
class RevokeInvitationInput:
    invitation_id: strawberry.ID


@strawberry.input
class AcceptInvitationInput:
    token: str
    new_password: str


@strawberry.input
class SetStaffLoginAccessInput:
    user_id: strawberry.ID
    can_login: bool