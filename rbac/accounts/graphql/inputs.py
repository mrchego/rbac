import strawberry
from typing import List, Optional
from strawberry.file_uploads import Upload


@strawberry.input
class UpdateProfileInput:
    """Self-service profile update — no email, no company, no auth flags."""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    avatar: Optional[Upload] = None


@strawberry.input
class AdminUpdateUserInput:
    """Owner-level update of another user's basic profile fields."""
    user_id: strawberry.ID
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    avatar: Optional[Upload] = None


@strawberry.input
class UserIdInput:
    """Shared shape for the simple id-only admin actions."""
    user_id: strawberry.ID


@strawberry.input
class LockUserInput:
    user_id: strawberry.ID
    duration_minutes: int = 15
    
@strawberry.input
class BulkUserIdsInput:
    user_ids: List[strawberry.ID]


@strawberry.input
class BulkLockUsersInput:
    user_ids: List[strawberry.ID]
    duration_minutes: int = 15
    
    
# accounts/graphql/inputs.py — add these

@strawberry.input
class PromoteToOwnerInput:
    user_id: strawberry.ID


@strawberry.input
class DemoteOwnerInput:
    user_id: strawberry.ID