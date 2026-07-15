from rbac.accounts.selectors import get_user_by_email
from rbac.identity.services.send_email_verification_code import send_email_verification_code


def request_email_verification(*, email: str):
    user = get_user_by_email(email=email)
    if user and not user.is_email_verified:
        send_email_verification_code(user=user)
    # Always return True — never reveal whether the email exists or is already verified.
    return True