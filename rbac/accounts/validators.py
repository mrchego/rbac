from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_password_strength(password: str) -> None:
    """Validates that the password meets minimum security requirements."""
    if len(password) < 8:
        raise ValidationError(_("Password must be at least 8 characters long."))
    # Add future requirements easily here (uppercase, lowercase, digit, etc.)