from typing import List, Optional
import strawberry
from rbac.core.graphql.errors import MutationError

@strawberry.type
class SimpleMutationPayload:
    success: bool
    errors: Optional[List[MutationError]] = None