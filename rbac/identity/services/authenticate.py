from django.contrib.auth import authenticate as django_authenticate
from rbac.core.exceptions import ApplicationError, ErrorCode

def authenticate_credentials(*, email: str, password: str):
    user = django_authenticate(email=email, password=password)
    if not user:
        raise ApplicationError(
            "Invalid email or password.", 
            code=ErrorCode.INVALID_CREDENTIALS
        )
    return user