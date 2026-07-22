import strawberry
import strawberry_django
from strawberry import auto
from typing import List

from rbac.accounts.graphql.types import UserType
from rbac.authorization.models import Permission, Role, UserPermissionOverride

@strawberry_django.type(Permission)
class PermissionType:
    id: auto
    codename: auto
    label: auto
    category: auto


@strawberry_django.type(Role)
class RoleType:
    id: auto
    name: auto
    is_default: auto
    created_at: auto
    updated_at: auto

    @strawberry.field
    def permissions(self) -> List[PermissionType]:
        return list(self.permissions.all())

    @strawberry.field
    def staff_count(self) -> int:
        return self.user_roles.count()
    
    @strawberry.field
    def assigned_users(self) -> List["UserType"]:
        from rbac.accounts.graphql.types import UserType
        return [ur.user for ur in self.user_roles.select_related("user").all()]


@strawberry_django.type(UserPermissionOverride)
class UserPermissionOverrideType:
    id: auto
    is_granted: auto

    @strawberry.field
    def permission(self) -> PermissionType:
        return self.permission


@strawberry.type
class EffectivePermissionsType:
    """What a specific user can actually do right now — roles + overrides collapsed into one list."""
    user_id: strawberry.ID
    codenames: List[str]