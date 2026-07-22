import strawberry
from rbac.authorization.graphql.inputs import (
    CreateRoleInput,
    UpdateRoleInput,
    DeleteRoleInput,
    CloneRoleInput,
    AssignRoleInput,
    RemoveRoleInput,
    BulkAssignRoleInput,
    BulkRemoveRoleInput,
    SetPermissionOverrideInput,
    ClearPermissionOverrideInput,
)
from rbac.authorization.graphql.payloads import (
    RoleMutationPayload,
    AssignmentMutationPayload,
)
from rbac.core.graphql.payloads import BulkActionPayload, to_bulk_payload
from rbac.authorization.services.create_role import create_role as create_role_action
from rbac.authorization.services.update_role import update_role as update_role_action
from rbac.authorization.services.delete_role import delete_role as delete_role_action
from rbac.authorization.services.clone_role import clone_role as clone_role_action
from rbac.authorization.services.assign_role import assign_role as assign_role_action
from rbac.authorization.services.remove_role import remove_role as remove_role_action
from rbac.authorization.services.bulk_assign_role import (
    bulk_assign_role as bulk_assign_role_action,
)
from rbac.authorization.services.bulk_remove_role import (
    bulk_remove_role as bulk_remove_role_action,
)
from rbac.authorization.services.set_permission_override import (
    set_permission_override as set_override_action,
    clear_permission_override as clear_override_action,
)
from rbac.accounts.selectors import get_current_user
from rbac.core.exceptions import ApplicationError, AppPermissionDeniedError
from rbac.core.graphql.errors import format_application_error
from rbac.authorization.decorators import require_owner


@strawberry.type
class RoleMutation:
    @strawberry.mutation
    @require_owner()
    def create_role(
        self, info: strawberry.Info, input: CreateRoleInput
    ) -> RoleMutationPayload:
        current = get_current_user(info)
        if not current or not current.company_id:
            raise AppPermissionDeniedError("No company context.")
        try:
            role = create_role_action(
                company=current.company,
                name=input.name,
                permission_codenames=input.permission_codenames,
                is_default=input.is_default,
            )
            return RoleMutationPayload(success=True, role=role)
        except ApplicationError as e:
            return RoleMutationPayload(
                success=False, errors=[format_application_error(e)]
            )

    @strawberry.mutation
    @require_owner()
    def update_role(
        self, info: strawberry.Info, input: UpdateRoleInput
    ) -> RoleMutationPayload:
        current = get_current_user(info)
        if not current or not current.company_id:
            raise AppPermissionDeniedError("No company context.")
        try:
            role = update_role_action(
                role_id=input.role_id,
                company_id=str(current.company_id),
                name=input.name,
                permission_codenames=input.permission_codenames,
                is_default=input.is_default,
            )
            return RoleMutationPayload(success=True, role=role)
        except ApplicationError as e:
            return RoleMutationPayload(
                success=False, errors=[format_application_error(e)]
            )

    @strawberry.mutation
    @require_owner()
    def delete_role(
        self, info: strawberry.Info, input: DeleteRoleInput
    ) -> AssignmentMutationPayload:
        current = get_current_user(info)
        if not current or not current.company_id:
            raise AppPermissionDeniedError("No company context.")
        try:
            delete_role_action(
                role_id=input.role_id, company_id=str(current.company_id)
            )
            return AssignmentMutationPayload(success=True)
        except ApplicationError as e:
            return AssignmentMutationPayload(
                success=False, errors=[format_application_error(e)]
            )

    @strawberry.mutation
    @require_owner()
    def clone_role(
        self, info: strawberry.Info, input: CloneRoleInput
    ) -> RoleMutationPayload:
        current = get_current_user(info)
        if not current or not current.company_id:
            raise AppPermissionDeniedError("No company context.")
        try:
            role = clone_role_action(
                role_id=input.role_id,
                company_id=str(current.company_id),
                new_name=input.new_name,
            )
            return RoleMutationPayload(success=True, role=role)
        except ApplicationError as e:
            return RoleMutationPayload(
                success=False, errors=[format_application_error(e)]
            )

    @strawberry.mutation
    @require_owner()
    def assign_role(self, info: strawberry.Info, input: AssignRoleInput) -> AssignmentMutationPayload:
        current = get_current_user(info)
        if not current or not current.company_id:
            raise AppPermissionDeniedError("No company context.")
        try:
            assign_role_action(user_id=input.user_id, role_id=input.role_id, company_id=str(current.company_id))
            return AssignmentMutationPayload(success=True)
        except ApplicationError as e:
            return AssignmentMutationPayload(success=False, errors=[format_application_error(e)])

    @strawberry.mutation
    @require_owner()
    def remove_role(self, info: strawberry.Info, input: RemoveRoleInput) -> AssignmentMutationPayload:
        current = get_current_user(info)
        if not current or not current.company_id:
            raise AppPermissionDeniedError("No company context.")
        try:
            remove_role_action(user_id=input.user_id, role_id=input.role_id, company_id=str(current.company_id))
            return AssignmentMutationPayload(success=True)
        except ApplicationError as e:
            return AssignmentMutationPayload(success=False, errors=[format_application_error(e)])

    @strawberry.mutation
    @require_owner()
    def bulk_assign_role(
        self, info: strawberry.Info, input: BulkAssignRoleInput
    ) -> BulkActionPayload:
        current = get_current_user(info)
        if not current or not current.company_id:
            raise AppPermissionDeniedError("No company context.")
        result = bulk_assign_role_action(
            user_ids=input.user_ids,
            role_id=input.role_id,
            company_id=str(current.company_id),
        )
        return to_bulk_payload(result)

    @strawberry.mutation
    @require_owner()
    def bulk_remove_role(
        self, info: strawberry.Info, input: BulkRemoveRoleInput
    ) -> BulkActionPayload:
        current = get_current_user(info)
        if not current or not current.company_id:
            raise AppPermissionDeniedError("No company context.")
        result = bulk_remove_role_action(
            user_ids=input.user_ids,
            role_id=input.role_id,
            company_id=str(current.company_id),
        )
        return to_bulk_payload(result)

    @strawberry.mutation
    @require_owner()
    def set_permission_override(
        self, info: strawberry.Info, input: SetPermissionOverrideInput
    ) -> AssignmentMutationPayload:
        try:
            set_override_action(
                user_id=input.user_id,
                permission_codename=input.permission_codename,
                is_granted=input.is_granted,
            )
            return AssignmentMutationPayload(success=True)
        except ApplicationError as e:
            return AssignmentMutationPayload(
                success=False, errors=[format_application_error(e)]
            )

    @strawberry.mutation
    @require_owner()
    def clear_permission_override(
        self, info: strawberry.Info, input: ClearPermissionOverrideInput
    ) -> AssignmentMutationPayload:
        try:
            clear_override_action(
                user_id=input.user_id, permission_codename=input.permission_codename
            )
            return AssignmentMutationPayload(success=True)
        except ApplicationError as e:
            return AssignmentMutationPayload(
                success=False, errors=[format_application_error(e)]
            )
