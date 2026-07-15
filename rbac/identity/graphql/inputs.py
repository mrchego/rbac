import strawberry


@strawberry.input
class LoginInput:
    email: str
    password: str


# @strawberry.input
# class LogoutInput:
#     pass


@strawberry.input
class RequestEmailVerificationInput:
    email: str


@strawberry.input
class VerifyEmailCodeInput:
    email: str
    code: str


@strawberry.input
class ForgotPasswordInput:
    email: str


@strawberry.input
class ResetPasswordInput:
    email: str
    code: str
    new_password: str


@strawberry.input
class ChangePasswordInput:
    current_password: str
    new_password: str