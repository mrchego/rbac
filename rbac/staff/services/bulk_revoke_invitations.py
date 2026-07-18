from django.db import transaction
from rbac.staff.models import Invitation
from rbac.accounts.services.bulk_result import BulkActionResult


@transaction.atomic
def bulk_revoke_invitations(*, invitation_ids, company_id):
    result = BulkActionResult()
    invitation_ids = [str(iid) for iid in invitation_ids]
    invitations = list(Invitation.objects.filter(pk__in=invitation_ids, company_id=company_id))
    found_ids = {str(inv.id) for inv in invitations}

    for invitation in invitations:
        iid = str(invitation.id)
        if invitation.used:
            result.add_failure(iid, "Already used.")
            continue

        # Same cleanup as the single-record revoke_invitation — don't leave
        # a dangling, never-activated placeholder user behind.
        user = invitation.company.users.filter(email=invitation.email, is_active=False).first()
        if user:
            user.delete()
        invitation.delete()
        result.add_success(iid)

    for missing in set(invitation_ids) - found_ids:
        result.add_failure(missing, "Invitation not found in this company.")

    return result