import strawberry

from rbac.staff.graphql.inputs import (
    InviteStaffInput,
    RevokeInvitationInput,
    AcceptInvitationInput,
    SetStaffLoginAccessInput,
    PromoteStaffToLoginInput,
    ResendInvitationInput,
    BulkRevokeInvitationsInput,
    DemoteStaffFromLoginInput,
)
from rbac.staff.graphql.payloads import (
    InvitationMutationPayload,
    AcceptInvitationPayload,
    BulkInvitationActionPayload,
)
from rbac.core.graphql.payloads import SimpleMutationPayload
from rbac.staff.services import (
    revoke_invitation as revoke_invitation_action,
    set_staff_login_access as set_staff_login_access_action,
    resend_invitation as resend_invitation_action,
    bulk_revoke_invitations as bulk_revoke_invitations_action,
    demote_staff_from_login as demote_staff_from_login_action,
)
from rbac.staff.workflows import (
    accept_invitation as accept_invitation_action,
    invite_staff as invite_staff_action,
    promote_staff_to_login as promote_staff_to_login_action,
)
from rbac.accounts.selectors import get_current_user
from rbac.accounts.graphql.payloads import BulkActionFailure
from rbac.authorization.decorators import require_owner
from rbac.authorization.models import Role
from rbac.core.exceptions import ApplicationError, AppPermissionDeniedError
from rbac.core.graphql.errors import format_application_error


def _to_bulk_invitation_payload(result) -> BulkInvitationActionPayload:
    return BulkInvitationActionPayload(
        success=len(result.failed) == 0,
        succeeded_ids=result.succeeded,
        failed=[
            BulkActionFailure(user_id=f["user_id"], reason=f["reason"])
            for f in result.failed
        ],
    )


@strawberry.type
class StaffMutation:
    @strawberry.mutation
    @require_owner()
    def invite_staff(
        self, info: strawberry.Info, input: InviteStaffInput
    ) -> InvitationMutationPayload:
        current = get_current_user(info)
        try:
            role = None
            if input.can_login and input.role_id:
                role = Role.objects.filter(
                    pk=input.role_id, company=current.company
                ).first()
                if not role:
                    raise ApplicationError("Role not found.", code="ROLE_NOT_FOUND")

            _, invitation = invite_staff_action(
                email=input.email,
                first_name=input.first_name,
                last_name=input.last_name,
                company=current.company,
                invited_by=current,
                request=info.context.request,
                can_login=input.can_login,
                role=role,
            )
            return InvitationMutationPayload(success=True, invitation=invitation)
        except ApplicationError as e:
            return InvitationMutationPayload(
                success=False, errors=[format_application_error(e)]
            )

    @strawberry.mutation
    @require_owner()
    def revoke_invitation(
        self, info: strawberry.Info, input: RevokeInvitationInput
    ) -> SimpleMutationPayload:
        try:
            revoke_invitation_action(invitation_id=input.invitation_id)
            return SimpleMutationPayload(success=True)
        except ApplicationError as e:
            return SimpleMutationPayload(
                success=False, errors=[format_application_error(e)]
            )

    @strawberry.mutation
    @require_owner()
    def resend_invitation(
        self, info: strawberry.Info, input: ResendInvitationInput
    ) -> InvitationMutationPayload:
        try:
            invitation = resend_invitation_action(
                invitation_id=input.invitation_id, request=info.context.request
            )
            return InvitationMutationPayload(success=True, invitation=invitation)
        except ApplicationError as e:
            return InvitationMutationPayload(
                success=False, errors=[format_application_error(e)]
            )

    @strawberry.mutation
    @require_owner()
    def bulk_revoke_invitations(
        self, info: strawberry.Info, input: BulkRevokeInvitationsInput
    ) -> BulkInvitationActionPayload:
        current = get_current_user(info)
        if not current or not current.company_id:
            raise AppPermissionDeniedError("No company context.")
        result = bulk_revoke_invitations_action(
            invitation_ids=input.invitation_ids, company_id=str(current.company_id)
        )
        return _to_bulk_invitation_payload(result)

    @strawberry.mutation
    @require_owner()
    def set_staff_login_access(
        self, info: strawberry.Info, input: SetStaffLoginAccessInput
    ) -> SimpleMutationPayload:
        try:
            set_staff_login_access_action(
                user_id=input.user_id, can_login=input.can_login
            )
            return SimpleMutationPayload(success=True)
        except ApplicationError as e:
            return SimpleMutationPayload(
                success=False, errors=[format_application_error(e)]
            )

    @strawberry.mutation
    @require_owner()
    def demote_staff_from_login(
        self, info: strawberry.Info, input: DemoteStaffFromLoginInput
    ) -> SimpleMutationPayload:
        current = get_current_user(info)
        if not current or not current.company_id:
            raise AppPermissionDeniedError("No company context.")
        try:
            demote_staff_from_login_action(
                user_id=input.user_id, company_id=str(current.company_id)
            )
            return SimpleMutationPayload(success=True)
        except ApplicationError as e:
            return SimpleMutationPayload(
                success=False, errors=[format_application_error(e)]
            )

    @strawberry.mutation
    def accept_invitation(
        self, info: strawberry.Info, input: AcceptInvitationInput
    ) -> AcceptInvitationPayload:
        try:
            user = accept_invitation_action(
                token=input.token, new_password=input.new_password
            )
            return AcceptInvitationPayload(success=True, user=user)
        except ApplicationError as e:
            return AcceptInvitationPayload(
                success=False, errors=[format_application_error(e)]
            )

    @strawberry.mutation
    @require_owner()
    def promote_staff_to_login(
        self, info: strawberry.Info, input: PromoteStaffToLoginInput
    ) -> InvitationMutationPayload:
        current = get_current_user(info)
        if not current or not current.company_id:
            raise AppPermissionDeniedError("No company context.")
        try:
            role = Role.objects.filter(
                pk=input.role_id, company=current.company
            ).first()
            if not role:
                raise ApplicationError("Role not found.", code="ROLE_NOT_FOUND")

            _, invitation = promote_staff_to_login_action(
                user_id=input.user_id,
                company=current.company,
                role=role,
                invited_by=current,
                request=info.context.request,
            )
            return InvitationMutationPayload(success=True, invitation=invitation)
        except ApplicationError as e:
            return InvitationMutationPayload(
                success=False, errors=[format_application_error(e)]
            )
