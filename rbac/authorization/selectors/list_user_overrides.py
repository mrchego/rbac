from rbac.authorization.models import UserPermissionOverride


def list_user_overrides(*, user_id: str):
    return UserPermissionOverride.objects.filter(user_id=user_id).select_related("permission")