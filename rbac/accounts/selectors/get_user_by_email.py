# rbac/accounts/selectors/get_user_by_email.py
from typing import Optional
from rbac.accounts.models import User

def get_user_by_email(*, email: str) -> Optional[User]:
    return User.objects.filter(email=email).first()