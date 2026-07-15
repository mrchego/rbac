import strawberry
from typing import Optional
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