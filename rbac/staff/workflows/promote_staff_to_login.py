from django.db import transaction
from django.utils import timezone
from rbac.accounts.selectors import get_user
from rbac.authorization.models import UserRole
from rbac.staff.models import Invitation
from rbac.staff.constants import INVITATION_EXPIRY_DAYS
from rbac.staff.selectors import get_pending_invitation_for_email
from rbac.staff.services.send_invitation_email import send_invitation_email
from rbac.core.exceptions import ApplicationError, ErrorCode


@transaction.atomic
def promote_staff_to_login(*, user_id, company, role, invited_by, request):
    user = get_user(user_id=user_id)
    if not user or user.company_id != company.id:
        raise ApplicationError("Staff member not found.", code=ErrorCode.USER_NOT_FOUND)

    if user.can_login:
        raise ApplicationError(
            "This staff member can already log in.", code=ErrorCode.VALIDATION_ERROR
        )

    if get_pending_invitation_for_email(email=user.email, company_id=company.id):
        raise ApplicationError(
            "An invitation is already pending for this staff member.",
            code=ErrorCode.VALIDATION_ERROR,
        )

    UserRole.objects.create(user=user, role=role)

    invitation = Invitation.objects.create(
        email=user.email,
        company=company,
        invited_by=invited_by,
        role=role,
        expires_at=timezone.now() + timezone.timedelta(days=INVITATION_EXPIRY_DAYS),
    )
    send_invitation_email(request=request, invitation=invitation)
    return user, invitation
