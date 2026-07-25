from django.template.loader import render_to_string

from rbac.core.tasks import send_email_task
from rbac.identity.constants import VERIFICATION_CODE_EXPIRY_MINUTES
from rbac.identity.models import VerificationCode
from rbac.identity.services.generate_verification_code import generate_verification_code


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
    send_email_task.delay(
        subject="Your password reset code",
        message=message,
        recipient_list=[user.email],
    )
    return True