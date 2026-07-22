import strawberry

from rbac.accounts.graphql.inputs import (
    UpdateProfileInput,
    AdminUpdateUserInput,
    UserIdInput,
    LockUserInput,
    BulkUserIdsInput,
    BulkLockUsersInput,
)
from rbac.accounts.graphql.payloads import UserMutationPayload
from rbac.core.graphql.payloads import BulkActionPayload, to_bulk_payload
from rbac.accounts.graphql.payloads import UserMutationPayload
from rbac.core.graphql.payloads import SimpleMutationPayload
from rbac.accounts.selectors import get_current_user
from rbac.accounts.services import (
    update_user,
    activate_user,
    deactivate_user,
    delete_user,
    lock_user,
    unlock_user,
    force_password_reset,
    bulk_activate_users,
    bulk_deactivate_users,
    bulk_delete_users,
    bulk_lock_users,
    bulk_unlock_users,
    bulk_force_password_reset,
    restore_user,
    bulk_restore_users,
)
from rbac.authorization.decorators import require_owner
from rbac.core.exceptions import ApplicationError, AppPermissionDeniedError
from rbac.core.graphql.errors import format_application_error


@strawberry.type
class UserMutation:
    @strawberry.mutation
    def update_profile(
        self, info: strawberry.Info, input: UpdateProfileInput
    ) -> UserMutationPayload:
        current = get_current_user(info)
        if not current:
            raise AppPermissionDeniedError("Authentication required.")
        try:
            kwargs = {
                k: v
                for k, v in {
                    "first_name": input.first_name,
                    "last_name": input.last_name,
                    "phone": input.phone,
                    "avatar": input.avatar,
                }.items()
                if v is not None
            }
            user = update_user(user_id=current.id, **kwargs)
            return UserMutationPayload(success=True, user=user)
        except ApplicationError as e:
            return UserMutationPayload(
                success=False, errors=[format_application_error(e)]
            )

    @strawberry.mutation
    @require_owner()
    def admin_update_user(
        self, info: strawberry.Info, input: AdminUpdateUserInput
    ) -> UserMutationPayload:
        try:
            kwargs = {
                k: v
                for k, v in {
                    "first_name": input.first_name,
                    "last_name": input.last_name,
                    "phone": input.phone,
                    "avatar": input.avatar,
                }.items()
                if v is not None
            }
            user = update_user(user_id=input.user_id, **kwargs)
            return UserMutationPayload(success=True, user=user)
        except ApplicationError as e:
            return UserMutationPayload(
                success=False, errors=[format_application_error(e)]
            )

    @strawberry.mutation
    @require_owner()
    def activate_user(
        self, info: strawberry.Info, input: UserIdInput
    ) -> SimpleMutationPayload:
        try:
            activate_user(user_id=input.user_id)
            return SimpleMutationPayload(success=True)
        except ApplicationError as e:
            return SimpleMutationPayload(
                success=False, errors=[format_application_error(e)]
            )

    @strawberry.mutation
    @require_owner()
    def deactivate_user(
        self, info: strawberry.Info, input: UserIdInput
    ) -> SimpleMutationPayload:
        try:
            deactivate_user(user_id=input.user_id)
            return SimpleMutationPayload(success=True)
        except ApplicationError as e:
            return SimpleMutationPayload(
                success=False, errors=[format_application_error(e)]
            )

    @strawberry.mutation
    @require_owner()
    def delete_user(
        self, info: strawberry.Info, input: UserIdInput
    ) -> SimpleMutationPayload:
        try:
            delete_user(user_id=input.user_id)
            return SimpleMutationPayload(success=True)
        except ApplicationError as e:
            return SimpleMutationPayload(
                success=False, errors=[format_application_error(e)]
            )

    @strawberry.mutation
    @require_owner()
    def lock_user(
        self, info: strawberry.Info, input: LockUserInput
    ) -> SimpleMutationPayload:
        try:
            lock_user(user_id=input.user_id, duration_minutes=input.duration_minutes)
            return SimpleMutationPayload(success=True)
        except ApplicationError as e:
            return SimpleMutationPayload(
                success=False, errors=[format_application_error(e)]
            )

    @strawberry.mutation
    @require_owner()
    def unlock_user(
        self, info: strawberry.Info, input: UserIdInput
    ) -> SimpleMutationPayload:
        try:
            unlock_user(user_id=input.user_id)
            return SimpleMutationPayload(success=True)
        except ApplicationError as e:
            return SimpleMutationPayload(
                success=False, errors=[format_application_error(e)]
            )

    @strawberry.mutation
    @require_owner()
    def force_password_reset(
        self, info: strawberry.Info, input: UserIdInput
    ) -> SimpleMutationPayload:
        try:
            force_password_reset(user_id=input.user_id)
            return SimpleMutationPayload(success=True)
        except ApplicationError as e:
            return SimpleMutationPayload(
                success=False, errors=[format_application_error(e)]
            )

    @strawberry.mutation
    @require_owner()
    def bulk_activate_users(
        self, info: strawberry.Info, input: BulkUserIdsInput
    ) -> BulkActionPayload:
        current = get_current_user(info)
        if not current or not current.company_id:
            raise AppPermissionDeniedError("No company context.")
        result = bulk_activate_users(
            user_ids=input.user_ids, company_id=str(current.company_id)
        )
        return to_bulk_payload(result)

    @strawberry.mutation
    @require_owner()
    def bulk_deactivate_users(
        self, info: strawberry.Info, input: BulkUserIdsInput
    ) -> BulkActionPayload:
        current = get_current_user(info)
        if not current or not current.company_id:
            raise AppPermissionDeniedError("No company context.")
        result = bulk_deactivate_users(
            user_ids=input.user_ids,
            company_id=str(current.company_id),
            current_user_id=current.id,
        )
        return to_bulk_payload(result)

    @strawberry.mutation
    @require_owner()
    def bulk_delete_users(
        self, info: strawberry.Info, input: BulkUserIdsInput
    ) -> BulkActionPayload:
        current = get_current_user(info)
        if not current or not current.company_id:
            raise AppPermissionDeniedError("No company context.")
        result = bulk_delete_users(
            user_ids=input.user_ids,
            company_id=str(current.company_id),
            current_user_id=current.id,
        )
        return to_bulk_payload(result)

    @strawberry.mutation
    @require_owner()
    def bulk_lock_users(
        self, info: strawberry.Info, input: BulkLockUsersInput
    ) -> BulkActionPayload:
        current = get_current_user(info)
        if not current or not current.company_id:
            raise AppPermissionDeniedError("No company context.")
        result = bulk_lock_users(
            user_ids=input.user_ids,
            company_id=str(current.company_id),
            current_user_id=current.id,
            duration_minutes=input.duration_minutes,
        )
        return to_bulk_payload(result)

    @strawberry.mutation
    @require_owner()
    def bulk_unlock_users(
        self, info: strawberry.Info, input: BulkUserIdsInput
    ) -> BulkActionPayload:
        current = get_current_user(info)
        if not current or not current.company_id:
            raise AppPermissionDeniedError("No company context.")
        result = bulk_unlock_users(
            user_ids=input.user_ids, company_id=str(current.company_id)
        )
        return to_bulk_payload(result)

    @strawberry.mutation
    @require_owner()
    def bulk_force_password_reset(
        self, info: strawberry.Info, input: BulkUserIdsInput
    ) -> BulkActionPayload:
        current = get_current_user(info)
        if not current or not current.company_id:
            raise AppPermissionDeniedError("No company context.")
        result = bulk_force_password_reset(
            user_ids=input.user_ids, company_id=str(current.company_id)
        )
        return to_bulk_payload(result)

    @strawberry.mutation
    @require_owner()
    def restore_user(
        self, info: strawberry.Info, input: UserIdInput
    ) -> SimpleMutationPayload:
        try:
            restore_user(user_id=input.user_id)
            return SimpleMutationPayload(success=True)
        except ApplicationError as e:
            return SimpleMutationPayload(
                success=False, errors=[format_application_error(e)]
            )

    @strawberry.mutation
    @require_owner()
    def bulk_restore_users(
        self, info: strawberry.Info, input: BulkUserIdsInput
    ) -> BulkActionPayload:
        current = get_current_user(info)
        if not current or not current.company_id:
            raise AppPermissionDeniedError("No company context.")
        result = bulk_restore_users(
            user_ids=input.user_ids, company_id=str(current.company_id)
        )
        return to_bulk_payload(result)
