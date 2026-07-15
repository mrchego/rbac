from typing import Optional
from rbac.staff.models import Invitation


def get_invitation_by_token(*, token: str) -> Optional[Invitation]:
    return Invitation.objects.filter(token=token, used=False).first()