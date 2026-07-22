from functools import wraps
from rbac.core.exceptions import AppPermissionDeniedError
from rbac.authorization.selectors.user_has_permission import user_has_permission


def require_permission(codename):
    def decorator(resolver):
        @wraps(resolver)
        def wrapper(self, info, *args, **kwargs):
            user = info.context.request.user
            if not user.is_authenticated:
                raise AppPermissionDeniedError("Authentication required.")
            if not user_has_permission(user=user, codename=codename):
                raise AppPermissionDeniedError(f"Missing permission: {codename}")
            return resolver(self, info, *args, **kwargs)

        return wrapper

    return decorator


def require_owner():
    """For company-owner-only actions: managing roles, inviting staff, etc."""

    def decorator(resolver):
        @wraps(resolver)
        def wrapper(self, info, *args, **kwargs):
            user = info.context.request.user
            if not user.is_authenticated:
                raise AppPermissionDeniedError("Authentication required.")
            if not user.is_superuser:
                raise AppPermissionDeniedError(
                    "Only the company owner can perform this action."
                )
            return resolver(self, info, *args, **kwargs)

        return wrapper

    return decorator
