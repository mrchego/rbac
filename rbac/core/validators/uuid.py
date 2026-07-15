import uuid
from django.core.exceptions import ValidationError

def validate_uuid(value):
    try:
        uuid.UUID(str(value))
    except (ValueError, TypeError):
        raise ValidationError("Invalid UUID format.")
    return value