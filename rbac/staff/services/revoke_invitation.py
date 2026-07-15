from django.db import transaction
from rbac.staff.models import Invitation
from rbac.core.exceptions import ApplicationError, ErrorCode


@transaction.atomic
def revoke_invitation(*, invitation_id):
    invitation = Invitation.objects.filter(pk=invitation_id, used=False).first()
    if not invitation:
        raise ApplicationError("Invitation not found or already used.", code=ErrorCode.VALIDATION_ERROR)

    # Delete the still-inactive placeholder user created at invite time too,
    # so a revoked invite doesn't leave a dangling, never-activated account.
    user = invitation.company.users.filter(email=invitation.email, is_active=False).first()
    if user:
        user.delete()

    invitation.delete()
    return True