import strawberry
from typing import List, Optional

from rbac.authorization.graphql.types import (
    PermissionType,
    RoleType,
    EffectivePermissionsType,
)
from rbac.authorization.selectors.get_role import get_role
from rbac.authorization.selectors.list_roles import list_roles
from rbac.authorization.selectors.get_permission import list_permissions
from rbac.authorization.selectors.get_user_permissions import (
    get_user_permission_codenames,
)
from rbac.authorization.selectors.list_user_overrides import list_user_overrides
from rbac.authorization.graphql.types import UserPermissionOverrideType
from rbac.accounts.selectors import get_current_user, get_user
from rbac.core.exceptions import AppPermissionDeniedError
from rbac.authorization.selectors.user_has_permission import user_has_permission

@strawberry.type
class RoleQuery:
    @strawberry.field
    def permissions(self, info: strawberry.Info) -> List[PermissionType]:
        """The full, code-defined permission catalog — for rendering the checkbox list."""
        return list(list_permissions())

    @strawberry.field
    def roles(self, info: strawberry.Info) -> List[RoleType]:
        current = get_current_user(info)
        if not current or not current.company_id:
            raise AppPermissionDeniedError("No company context.")
        return list(list_roles(company_id=str(current.company_id)))

    @strawberry.field
    def role(self, info: strawberry.Info, role_id: strawberry.ID) -> Optional[RoleType]:
        current = get_current_user(info)
        if not current or not current.company_id:
            raise AppPermissionDeniedError("No company context.")
        return get_role(role_id=role_id, company_id=str(current.company_id))

    @strawberry.field
    def effective_permissions(
        self, info: strawberry.Info, user_id: strawberry.ID
    ) -> EffectivePermissionsType:
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

    @strawberry.field
    def my_permissions(self, info: strawberry.Info) -> EffectivePermissionsType:
        current = get_current_user(info)
        if not current:
            raise AppPermissionDeniedError("Authentication required.")
        codenames = get_user_permission_codenames(user=current)
        return EffectivePermissionsType(user_id=current.id, codenames=sorted(codenames))
    
    @strawberry.field
    def user_permission_overrides(
        self, info: strawberry.Info, user_id: strawberry.ID
    ) -> List[UserPermissionOverrideType]:
        current = get_current_user(info)
        if not current:
            raise AppPermissionDeniedError("Authentication required.")
        if not current.is_superuser and str(current.id) != str(user_id):
            raise AppPermissionDeniedError("You can only view your own permission overrides.")
        return list(list_user_overrides(user_id=user_id))
    
    @strawberry.field
    def has_permission(self, info: strawberry.Info, codename: str) -> bool:
        current = get_current_user(info)
        if not current:
            raise AppPermissionDeniedError("Authentication required.")
        return user_has_permission(user=current, codename=codename)
