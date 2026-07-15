from django.utils import timezone
from rbac.accounts.services import unlock_user

def handle_successful_login(user):
    # Only unlock the user if they actually had a pending lock or failures
    if user.failed_login_attempts > 0 or user.locked_until:
        unlock_user(user_id=user.id)
    
    # Always update the last_login timestamp
    user.last_login = timezone.now()
    user.save(update_fields=['last_login'])