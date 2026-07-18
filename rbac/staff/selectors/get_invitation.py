from typing import Optional
from rbac.staff.models import Invitation


def get_invitation(*, invitation_id: str) -> Optional[Invitation]:
    return Invitation.objects.filter(pk=invitation_id).first()