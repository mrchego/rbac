import re
from rbac.core.constants import PHONE_REGEX
from rbac.core.exceptions import AppValidationError

def validate_phone_number(value):
    if not re.match(PHONE_REGEX, value):
        raise AppValidationError("Enter a valid phone number.", field="phone")
    return value