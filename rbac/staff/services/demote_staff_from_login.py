from django.db import transaction
from rbac.accounts.selectors import get_user
from rbac.authorization.models import UserRole
from rbac.staff.selectors import get_pending_invitation_for_email
from rbac.core.exceptions import ApplicationError, ErrorCode


@transaction.atomic
def demote_staff_from_login(*, user_id, company_id):
    """Reverses invite_staff(can_login=True) / promote_staff_to_login —
    strips role assignments and login access, and cancels any invitation
    still pending acceptance."""
    user = get_user(user_id=user_id)
    if not user or user.company_id != company_id:
        raise ApplicationError("Staff member not found.", code=ErrorCode.USER_NOT_FOUND)

    UserRole.objects.filter(user=user).delete()
    user.can_login = False
    user.save(update_fields=["can_login"])

    pending = get_pending_invitation_for_email(email=user.email, company_id=company_id)
    if pending:
        pending.delete()

    return user