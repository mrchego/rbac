from typing import List, Optional
import strawberry
from rbac.core.graphql.errors import MutationError

@strawberry.type
class SimpleMutationPayload:
    success: bool
    errors: Optional[List[MutationError]] = None
    
    
@strawberry.type
class BulkActionFailure:
    user_id: strawberry.ID
    reason: str


@strawberry.type
class BulkActionPayload:
    """success=True only if every row succeeded — succeeded_ids/failed are
    always populated, so the frontend can show partial results either way."""
    success: bool
    succeeded_ids: List[strawberry.ID]
    failed: List[BulkActionFailure]


def to_bulk_payload(result) -> BulkActionPayload:
    return BulkActionPayload(
        success=len(result.failed) == 0,
        succeeded_ids=result.succeeded,
        failed=[BulkActionFailure(user_id=f["user_id"], reason=f["reason"]) for f in result.failed],
    )