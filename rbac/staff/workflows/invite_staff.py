# rbac/staff/workflows/invite_staff.py
from django.db import transaction
from rbac.accounts.services import create_user
from rbac.staff.models import Invitation
from rbac.staff.services.send_invitation_email import send_invitation_email
from rbac.authorization.models import UserRole
from rbac.core.exceptions import ApplicationError, ErrorCode


@transaction.atomic
def invite_staff(*, email, first_name, last_name, company, invited_by, request,
                  can_login=True, role=None):
    from rbac.accounts.selectors import get_user_by_email
    existing = get_user_by_email(email=email)
    if existing and existing.is_active:
        raise ApplicationError("User with this email already active.", code=ErrorCode.USER_ALREADY_EXISTS)

    if can_login and role is None:
        raise ApplicationError("A role is required to grant login access.", code=ErrorCode.VALIDATION_ERROR)

    user = create_user(
        email=email, first_name=first_name, last_name=last_name,
        password=None, company=company, can_login=False,
        # audit-only staff are active immediately; login staff activate on invitation acceptance
        is_active=not can_login,
        is_staff=False,
    )

    invitation = None
    if can_login:
        UserRole.objects.create(user=user, role=role)
        invitation = Invitation.objects.create(
            email=email, company=company, invited_by=invited_by, role=role,
        )
        send_invitation_email(request=request, invitation=invitation)

    return user, invitation