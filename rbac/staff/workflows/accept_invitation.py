from django.db import transaction
from django.utils import timezone
from rbac.staff.models import Invitation
from rbac.identity.services import set_password_unchecked
from rbac.core.exceptions import ApplicationError, ErrorCode


@transaction.atomic
def accept_invitation(*, token, new_password):
    try:
        invitation = Invitation.objects.get(token=token, used=False)
    except Invitation.DoesNotExist:
        raise ApplicationError("Invalid or expired invitation token.", code=ErrorCode.INVALID_TOKEN)

    if invitation.is_expired:
        raise ApplicationError("This invitation has expired. Ask an admin to resend it.", code=ErrorCode.INVALID_TOKEN)

    user = invitation.company.users.filter(email=invitation.email).first()
    if not user:
        raise ApplicationError("User no longer exists.", code=ErrorCode.USER_NOT_FOUND)

    set_password_unchecked(user, new_password)
    user.can_login = True
    user.is_active = True
    user.save(update_fields=["can_login", "is_active"])

    invitation.used = True
    invitation.accepted_at = timezone.now()
    invitation.save(update_fields=["used", "accepted_at"])

    return user