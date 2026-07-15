def get_user_permission_codenames(*, user) -> set[str]:
    from rbac.authorization.models import UserRole, UserPermissionOverride

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

    return role_perms