from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from rbac.identity.models import VerificationCode
from rbac.identity.services.generate_verification_code import generate_verification_code
from rbac.identity.constants import VERIFICATION_CODE_EXPIRY_MINUTES


def send_password_reset_code(*, user):
    verification_code = generate_verification_code(
        user=user, purpose=VerificationCode.Purpose.PASSWORD_RESET
    )
    message = render_to_string(
        "identity/verification_code_email.txt",
        {
            "code": verification_code.code,
            "minutes": VERIFICATION_CODE_EXPIRY_MINUTES,
            "purpose_label": "password reset",
        },
    )
    send_mail(
        subject="Your password reset code",
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )
    return True