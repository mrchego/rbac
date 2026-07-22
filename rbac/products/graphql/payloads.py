import strawberry
from typing import Optional, List

from rbac.products.graphql.types import ProductType
from rbac.core.graphql.errors import MutationError
from rbac.core.graphql.payloads import BulkActionFailure, BulkActionPayload  # noqa: F401


@strawberry.type
class ProductMutationPayload:
    success: bool
    product: Optional[ProductType] = None
    errors: Optional[List[MutationError]] = None


# Kept as aliases so existing imports keep working.
ProductBulkActionFailure = BulkActionFailure
BulkProductActionPayload = BulkActionPayload