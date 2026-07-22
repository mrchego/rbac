def user_has_permission(*, user, codename: str) -> bool:
    if user.is_superuser:
        return True
    from rbac.authorization.selectors.get_user_permissions import get_user_permission_codenames
    return codename in get_user_permission_codenames(user=user)