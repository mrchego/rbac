from django.db import transaction
from rbac.accounts.selectors import get_user_by_email
from rbac.identity.models import VerificationCode
from rbac.identity.services.verify_code import verify_code
from rbac.identity.services.change_password import set_password_unchecked
from rbac.core.exceptions import ApplicationError, ErrorCode


@transaction.atomic
def reset_password(*, email: str, code: str, new_password: str):
    user = get_user_by_email(email=email)
    if not user:
        raise ApplicationError("Invalid email or code.", code=ErrorCode.INVALID_TOKEN)

    verify_code(user=user, code=code, purpose=VerificationCode.Purpose.PASSWORD_RESET)
    set_password_unchecked(user, new_password)
    return True