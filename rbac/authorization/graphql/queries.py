# rbac/authorization/graphql/queries.py
import strawberry
from typing import List

from rbac.authorization.graphql.types import PermissionType, RoleType, EffectivePermissionsType
from rbac.authorization.models import Permission, Role
from rbac.authorization.selectors.get_user_permissions import get_user_permission_codenames
from rbac.accounts.selectors import get_current_user
from rbac.company.selectors import get_company
from rbac.core.exceptions import AppPermissionDeniedError


@strawberry.type
class RoleQuery:
    @strawberry.field
    def permissions(self, info: strawberry.Info) -> List[PermissionType]:
        """The full, code-defined permission catalog — for rendering the checkbox list."""
        return list(Permission.objects.all())

    @strawberry.field
    def roles(self, info: strawberry.Info) -> List[RoleType]:
        company = get_company()
        return list(Role.objects.filter(company=company))

    @strawberry.field
    def effective_permissions(self, info: strawberry.Info, user_id: strawberry.ID) -> EffectivePermissionsType:
        from rbac.accounts.selectors import get_user

        current = get_current_user(info)
        if not current:
            raise AppPermissionDeniedError("Authentication required.")

        # Only the company owner can look up someone else's permissions —
        # everyone else can only ever query their own.
        if not current.is_superuser and str(current.id) != str(user_id):
            raise AppPermissionDeniedError("You can only view your own permissions.")

        user = get_user(user_id=user_id)
        codenames = get_user_permission_codenames(user=user) if user else set()
        return EffectivePermissionsType(user_id=user_id, codenames=sorted(codenames))