# rbac/identity/services/failed_login.py
from rbac.accounts.services import lock_user
from rbac.identity.constants import MAX_FAILED_ATTEMPTS, LOCKOUT_DURATION_MINUTES

def handle_failed_login(user):
    if not user:
        return

    user.failed_login_attempts += 1
    user.save(update_fields=['failed_login_attempts'])

    if user.failed_login_attempts >= MAX_FAILED_ATTEMPTS:
        lock_user(
            user_id=user.id,
            duration_minutes=LOCKOUT_DURATION_MINUTES,
        )