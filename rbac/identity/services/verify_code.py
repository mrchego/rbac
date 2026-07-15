import hmac
from django.db import transaction
from django.utils import timezone

from rbac.identity.models import VerificationCode
from rbac.core.exceptions import AppValidationError


@transaction.atomic
def verify_code(*, user, code, purpose):
    verification_code = (
        VerificationCode.objects.filter(user=user, purpose=purpose, used_at__isnull=True)
        .order_by("-created_at")
        .first()
    )
    if not verification_code:
        raise AppValidationError("No active verification code found. Request a new one.", field="code")

    if verification_code.is_expired:
        raise AppValidationError("This code has expired. Request a new one.", field="code")

    # Constant-time comparison — avoids leaking how many leading digits
    # matched via response-timing differences.
    if not hmac.compare_digest(verification_code.code, code):
        raise AppValidationError("Incorrect verification code.", field="code")

    verification_code.used_at = timezone.now()
    verification_code.save(update_fields=["used_at"])
    return True