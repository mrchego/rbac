from django.core.cache import cache

USER_PERMISSIONS_CACHE_TTL = 300  # seconds


def user_permissions_cache_key(*, user_id) -> str:
    return f"user_perms:{user_id}"


def invalidate_user_permissions_cache(*, user_id) -> None:
    """Call after anything that changes what a specific user can do:
    role assignment/removal, permission overrides, login access changes."""
    cache.delete(user_permissions_cache_key(user_id=user_id))


def invalidate_role_permissions_cache(*, role) -> None:
    """Call after a role's own permission set changes (update_role) —
    every user currently holding that role has a stale cached list."""
    user_ids = list(role.user_roles.values_list("user_id", flat=True))
    if user_ids:
        cache.delete_many([user_permissions_cache_key(user_id=uid) for uid in user_ids])


def get_user_permission_codenames(*, user) -> set[str]:
    from rbac.authorization.models import UserPermissionOverride, UserRole

    cache_key = user_permissions_cache_key(user_id=user.id)
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    role_perms = set(
        UserRole.objects.filter(user=user)
        .values_list("role__permissions__codename", flat=True)
    )
    role_perms.discard(None)

    overrides = UserPermissionOverride.objects.filter(user=user).select_related("permission")
    for o in overrides:
        if o.is_granted:
            role_perms.add(o.permission.codename)
        else:
            role_perms.discard(o.permission.codename)

    cache.set(cache_key, role_perms, timeout=USER_PERMISSIONS_CACHE_TTL)
    return role_perms