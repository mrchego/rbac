from django.db import transaction
from django.utils import timezone

from rbac.identity.constants import (
    VERIFICATION_CODE_LENGTH,
    VERIFICATION_CODE_EXPIRY_MINUTES,
)
from rbac.identity.models import VerificationCode
from rbac.core.utils.strings import generate_numeric_code


@transaction.atomic
def generate_verification_code(*, user, purpose):
    # Invalidate any still-unused codes of the same purpose first, so only
    # the most recently issued code is ever valid — an old code that leaked
    # (e.g. visible in an inbox on a shared device) stops working the moment
    # a new one is requested.
    VerificationCode.objects.filter(
        user=user, purpose=purpose, used_at__isnull=True
    ).update(used_at=timezone.now())

    code = generate_numeric_code(length=VERIFICATION_CODE_LENGTH)
    return VerificationCode.objects.create(
        user=user,
        purpose=purpose,
        code=code,
        expires_at=timezone.now()
        + timezone.timedelta(minutes=VERIFICATION_CODE_EXPIRY_MINUTES),
    )
