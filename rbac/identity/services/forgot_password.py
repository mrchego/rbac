from rbac.accounts.selectors import get_user_by_email
from rbac.identity.services.send_password_reset_code import send_password_reset_code


def forgot_password(*, email: str):
    user = get_user_by_email(email=email)
    if user:
        send_password_reset_code(user=user)
    # Always return True — never reveal whether the email exists.
    return True