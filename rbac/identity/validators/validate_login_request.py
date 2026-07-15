from django.core.exceptions import ValidationError
from rbac.core.validators.email import validate_email

def validate_login_request(*, email: str, password: str) -> None:
    """Raises ValidationError if email or password is invalid."""
    validate_email(email)  # reuse core email validator
    if not password or len(password) < 1:
        raise ValidationError("Password cannot be empty.")