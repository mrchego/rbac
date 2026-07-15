from django.db import transaction
from rbac.accounts.selectors import get_user_by_email
from rbac.identity.models import VerificationCode
from rbac.identity.services.verify_code import verify_code
from rbac.core.exceptions import ApplicationError, ErrorCode


@transaction.atomic
def verify_email(*, email: str, code: str):
    user = get_user_by_email(email=email)
    if not user:
        raise ApplicationError("Invalid email or code.", code=ErrorCode.INVALID_TOKEN)

    verify_code(user=user, code=code, purpose=VerificationCode.Purpose.EMAIL_VERIFICATION)

    user.is_email_verified = True
    user.save(update_fields=["is_email_verified"])
    return user