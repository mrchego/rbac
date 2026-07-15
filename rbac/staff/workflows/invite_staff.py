from django.db import transaction
from rbac.accounts.services import create_user
from rbac.staff.models import Invitation
from rbac.staff.services.send_invitation_email import send_invitation_email
from rbac.authorization.models import UserRole
from rbac.core.exceptions import ApplicationError, ErrorCode


@transaction.atomic
def invite_staff(*, email, first_name, last_name, company, invited_by, request, can_login=True, role=None):
    from rbac.accounts.selectors import get_user_by_email
    existing = get_user_by_email(email=email)
    if existing and existing.is_active:
        raise ApplicationError("User with this email already active.", code=ErrorCode.USER_ALREADY_EXISTS)

    if not can_login:
        # Records-only staff: no system access, so no role, no password,
        # no invitation email — this is just an HR-style data record.
        # Created active immediately since there's no acceptance step.
        user = create_user(
            email=email, first_name=first_name, last_name=last_name,
            password=None, company=company,
            can_login=False, is_active=True, is_staff=False,
        )
        return user, None

    # Operational staff: needs a role and must go through the invite/accept flow.
    user = create_user(
        email=email, first_name=first_name, last_name=last_name,
        password=None, company=company, can_login=False, is_active=False, is_staff=False,
    )

    if role is not None:
        UserRole.objects.create(user=user, role=role)

    invitation = Invitation.objects.create(
        email=email, company=company, invited_by=invited_by, role=role,
    )

    send_invitation_email(request=request, invitation=invitation)
    return user, invitation