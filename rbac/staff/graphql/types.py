import strawberry
import strawberry_django
from strawberry import auto

from rbac.staff.models import Invitation


@strawberry_django.type(Invitation)
class InvitationType:
    id: auto
    email: auto
    used: auto
    expires_at: auto
    accepted_at: auto
    created_at: auto

    @strawberry.field
    def role_name(self) -> str:
        return self.role.name if self.role else ""

    @strawberry.field
    def invited_by_email(self) -> str:
        return self.invited_by.email if self.invited_by else ""

    @strawberry.field
    def is_expired(self) -> bool:
        return self.is_expired