import strawberry
from typing import Optional, List

from rbac.categories.graphql.types import CategoryType
from rbac.core.graphql.errors import MutationError


@strawberry.type
class CategoryMutationPayload:
    success: bool
    category: Optional[CategoryType] = None
    errors: Optional[List[MutationError]] = None


