import strawberry
from typing import List, Optional


@strawberry.input
class CreateRoleInput:
    name: str
    permission_codenames: List[str] = strawberry.field(default_factory=list)
    is_default: bool = False


@strawberry.input
class UpdateRoleInput:
    role_id: strawberry.ID
    name: Optional[str] = None
    permission_codenames: Optional[List[str]] = None
    is_default: Optional[bool] = None


@strawberry.input
class DeleteRoleInput:
    role_id: strawberry.ID


@strawberry.input
class AssignRoleInput:
    user_id: strawberry.ID
    role_id: strawberry.ID


@strawberry.input
class RemoveRoleInput:
    user_id: strawberry.ID
    role_id: strawberry.ID


@strawberry.input
class SetPermissionOverrideInput:
    user_id: strawberry.ID
    permission_codename: str
    is_granted: bool  # True = grant, False = explicitly revoke


@strawberry.input
class ClearPermissionOverrideInput:
    user_id: strawberry.ID
    permission_codename: str
    
@strawberry.input
class CloneRoleInput:
    role_id: strawberry.ID
    new_name: str


@strawberry.input
class BulkAssignRoleInput:
    user_ids: List[strawberry.ID]
    role_id: strawberry.ID


@strawberry.input
class BulkRemoveRoleInput:
    user_ids: List[strawberry.ID]
    role_id: strawberry.ID