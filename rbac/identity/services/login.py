from rbac.accounts.selectors import get_user_by_email
from rbac.identity.services.authenticate import authenticate_credentials
from rbac.identity.services.failed_login import handle_failed_login
from rbac.identity.services.successful_login import handle_successful_login
from rbac.core.exceptions import ApplicationError, ErrorCode

def login(*, email: str, password: str):
    # 1. Find user first (used only to check business rules if they exist)
    user = get_user_by_email(email=email)

    # Check business rules ONLY if the user exists. If not, skip to authentication.
    if user:
        if user.is_locked:
            raise ApplicationError(
                f"Account locked until {user.locked_until.strftime('%Y-%m-%d %H:%M:%S')}.",
                code=ErrorCode.ACCOUNT_LOCKED,
            )
        if not user.can_login:
            raise ApplicationError("Account disabled.", code=ErrorCode.ACCOUNT_DISABLED)
        if not user.is_active:
            raise ApplicationError("Account inactive.", code=ErrorCode.ACCOUNT_INACTIVE)

    # 2. Authenticate credentials (pricey hash occurs here regardless of existence)
    try:
        user = authenticate_credentials(email=email, password=password)
    except ApplicationError as exc:
        # If user exists, increment their attempts. If not, handle_failed_login(None) just returns.
        handle_failed_login(user)
        raise exc  # Re-raise the original exception

    # 3. Success Flow
    handle_successful_login(user)

    return user