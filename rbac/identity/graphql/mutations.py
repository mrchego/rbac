import strawberry
from django.contrib.auth import login as django_login, logout as django_logout

from rbac.identity.graphql.inputs import (
    LoginInput,
    RequestEmailVerificationInput,
    VerifyEmailCodeInput,
    ForgotPasswordInput,
    ResetPasswordInput,
    ChangePasswordInput,
)
from rbac.identity.graphql.payloads import AuthMutationPayload
from rbac.core.graphql.payloads import SimpleMutationPayload
from rbac.identity.services import (
    login as login_action,
    logout as logout_action,
    request_email_verification as request_email_verification_action,
    verify_email as verify_email_action,
    forgot_password as forgot_password_action,
    reset_password as reset_password_action,
    change_password as change_password_action,
)
from rbac.accounts.selectors import get_current_user
from rbac.core.exceptions import ApplicationError, AppPermissionDeniedError
from rbac.core.graphql.errors import format_application_error


@strawberry.type
class AuthMutation:
    @strawberry.mutation
    def login(self, info: strawberry.Info, input: LoginInput) -> AuthMutationPayload:
        try:
            user = login_action(email=input.email, password=input.password)
            django_login(info.context.request, user)
            return AuthMutationPayload(success=True, user=user)
        except ApplicationError as e:
            return AuthMutationPayload(success=False, errors=[format_application_error(e)])

    @strawberry.mutation
    def logout(self, info: strawberry.Info) -> SimpleMutationPayload:
        logout_action()
        django_logout(info.context.request)
        return SimpleMutationPayload(success=True)

    @strawberry.mutation
    def request_email_verification(
        self, info: strawberry.Info, input: RequestEmailVerificationInput
    ) -> SimpleMutationPayload:
        request_email_verification_action(email=input.email)
        return SimpleMutationPayload(success=True)

    @strawberry.mutation
    def verify_email_code(self, info: strawberry.Info, input: VerifyEmailCodeInput) -> SimpleMutationPayload:
        try:
            verify_email_action(email=input.email, code=input.code)
            return SimpleMutationPayload(success=True)
        except ApplicationError as e:
            return SimpleMutationPayload(success=False, errors=[format_application_error(e)])

    @strawberry.mutation
    def forgot_password(self, info: strawberry.Info, input: ForgotPasswordInput) -> SimpleMutationPayload:
        forgot_password_action(email=input.email)
        return SimpleMutationPayload(success=True)

    @strawberry.mutation
    def reset_password(self, info: strawberry.Info, input: ResetPasswordInput) -> SimpleMutationPayload:
        try:
            reset_password_action(email=input.email, code=input.code, new_password=input.new_password)
            return SimpleMutationPayload(success=True)
        except ApplicationError as e:
            return SimpleMutationPayload(success=False, errors=[format_application_error(e)])

    @strawberry.mutation
    def change_password(self, info: strawberry.Info, input: ChangePasswordInput) -> SimpleMutationPayload:
        user = get_current_user(info)
        if not user:
            raise AppPermissionDeniedError("Authentication required.")
        try:
            change_password_action(user, input.current_password, input.new_password)
            return SimpleMutationPayload(success=True)
        except ApplicationError as e:
            return SimpleMutationPayload(success=False, errors=[format_application_error(e)])