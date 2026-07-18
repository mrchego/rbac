import strawberry
from typing import Optional, List

from rbac.products.graphql.types import ProductType
from rbac.core.graphql.errors import MutationError


@strawberry.type
class ProductMutationPayload:
    success: bool
    product: Optional[ProductType] = None
    errors: Optional[List[MutationError]] = None


@strawberry.type
class ProductBulkActionFailure:
    product_id: strawberry.ID
    reason: str


@strawberry.type
class BulkProductActionPayload:
    success: bool
    succeeded_ids: List[strawberry.ID]
    failed: List[ProductBulkActionFailure]
