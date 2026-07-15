# rbac/authorization/graphql/mutations.py
import strawberry
from rbac.authorization.graphql.inputs import (
    CreateRoleInput,
    UpdateRoleInput,
    DeleteRoleInput,
    AssignRoleInput,
    RemoveRoleInput,
    SetPermissionOverrideInput,
    ClearPermissionOverrideInput,
)
from rbac.authorization.graphql.payloads import (
    RoleMutationPayload,
    AssignmentMutationPayload,
)
from rbac.authorization.services.create_role import create_role as create_role_action
from rbac.authorization.services.update_role import update_role as update_role_action
from rbac.authorization.services.delete_role import delete_role as delete_role_action
from rbac.authorization.services.assign_role import assign_role as assign_role_action
from rbac.authorization.services.remove_role import remove_role as remove_role_action
from rbac.authorization.services.set_permission_override import (
    set_permission_override as set_override_action,
    clear_permission_override as clear_override_action,
)
from rbac.company.selectors import get_company
from rbac.core.exceptions import ApplicationError
from rbac.core.graphql.errors import format_application_error
from rbac.authorization.decorators import require_owner


@strawberry.type
class RoleMutation:
    @strawberry.mutation
    @require_owner()
    def create_role(self, info: strawberry.Info, input: CreateRoleInput) -> RoleMutationPayload:
        try:
            company = get_company()
            role = create_role_action(
                company=company,
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
    def update_role(self, info: strawberry.Info, input: UpdateRoleInput) -> RoleMutationPayload:
        try:
            role = update_role_action(
                role_id=input.role_id,
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
    def delete_role(self, info: strawberry.Info, input: DeleteRoleInput) -> AssignmentMutationPayload:
        try:
            delete_role_action(role_id=input.role_id)
            return AssignmentMutationPayload(success=True)
        except ApplicationError as e:
            return AssignmentMutationPayload(
                success=False, errors=[format_application_error(e)]
            )

    @strawberry.mutation
    @require_owner()
    def assign_role(self, info: strawberry.Info, input: AssignRoleInput) -> AssignmentMutationPayload:
        try:
            assign_role_action(user_id=input.user_id, role_id=input.role_id)
            return AssignmentMutationPayload(success=True)
        except ApplicationError as e:
            return AssignmentMutationPayload(
                success=False, errors=[format_application_error(e)]
            )

    @strawberry.mutation
    @require_owner()
    def remove_role(self, info: strawberry.Info, input: RemoveRoleInput) -> AssignmentMutationPayload:
        try:
            remove_role_action(user_id=input.user_id, role_id=input.role_id)
            return AssignmentMutationPayload(success=True)
        except ApplicationError as e:
            return AssignmentMutationPayload(
                success=False, errors=[format_application_error(e)]
            )

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