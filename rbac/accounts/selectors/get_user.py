from typing import Optional
from rbac.accounts.models import User

def get_user(*, user_id: str) -> Optional[User]:
    """Returns the user or None if not found."""
    return User.objects.filter(pk=user_id).first()
