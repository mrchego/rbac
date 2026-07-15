from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError

django_email_validator = EmailValidator()

def validate_email(value):
    try:
        django_email_validator(value)
    except ValidationError as e:
        raise ValidationError(e.message)
    return value