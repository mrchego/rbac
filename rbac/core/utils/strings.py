import secrets
import string

def generate_random_string(length=32):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(length))


def generate_numeric_code(length=6) -> str:
    """For OTP-style codes — digits only, so it's easy to read/type/dictate."""
    return ''.join(secrets.choice(string.digits) for _ in range(length))