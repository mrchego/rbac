import uuid
from django.db import transaction
from django.utils import timezone
from rbac.staff.selectors import get_invitation
from rbac.staff.constants import INVITATION_EXPIRY_DAYS
from rbac.staff.services.send_invitation_email import send_invitation_email
from rbac.core.exceptions import ApplicationError, ErrorCode


@transaction.atomic
def resend_invitation(*, invitation_id, request):
    invitation = get_invitation(invitation_id=invitation_id)
    if not invitation or invitation.used:
        raise ApplicationError(
            "Invitation not found or already used.", code=ErrorCode.VALIDATION_ERROR
        )

    invitation.token = uuid.uuid4()
    invitation.expires_at = timezone.now() + timezone.timedelta(
        days=INVITATION_EXPIRY_DAYS
    )
    invitation.save(update_fields=["token", "expires_at"])

    send_invitation_email(request=request, invitation=invitation)
    return invitation
