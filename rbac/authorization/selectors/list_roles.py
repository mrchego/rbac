from rbac.authorization.models import Role


def list_roles(*, company_id: str):
    # prefetch_related on permissions + user_roles__user means RoleType's
    # `permissions` and `assigned_users` fields don't fire a fresh query
    # per role when listing many roles.
    return (
        Role.objects.filter(company_id=company_id)
        .prefetch_related("permissions", "user_roles__user")
    )