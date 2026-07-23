# accounts/services/ownership_guard.py
from rbac.accounts.selectors import count_active_superusers
from rbac.core.exceptions import ApplicationError, ErrorCode


def assert_not_last_owner(*, user, company_id, action="modify"):
    """
    Call before deactivating, deleting, locking, or demoting a user.

    - Founders can never be targeted by this action, by anyone, ever.
    - Non-founder owners can be targeted UNLESS it would leave the company
      with zero active owners.
    - Non-owners are unaffected and return immediately.
    """
    if not user.is_superuser:
        return

    if user.is_founder:
        raise ApplicationError(
            f"The founder's account cannot be {action}.",
            code=ErrorCode.CANNOT_MODIFY_FOUNDER,
        )

    remaining = count_active_superusers(company_id=company_id, exclude_ids=[str(user.id)])
    if remaining == 0:
        raise ApplicationError(
            f"Cannot {action} the last active owner of the company.",
            code=ErrorCode.LAST_OWNER,
        )