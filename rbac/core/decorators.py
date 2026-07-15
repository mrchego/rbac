from functools import wraps

from rbac.core.exceptions import AppValidationError
from rbac.core.validators.uuid import validate_uuid


def require_valid_uuid(field_name='id'):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            value = kwargs.get(field_name)
            if value:
                try:
                    validate_uuid(value)
                except AppValidationError:
                    raise AppValidationError(f"Invalid {field_name} format.")
            return func(*args, **kwargs)
        return wrapper
    return decorator