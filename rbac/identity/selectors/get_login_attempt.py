from typing import Optional, List
from rbac.accounts.models import User

def get_login_attempt(*, user: User, since: Optional[int] = None) -> List:
    """
    Placeholder: Returns a list of recent failed login attempts.
    In the future, this could query a `LoginAttempt` model.
    """
    # For now, just return an empty list
    return []