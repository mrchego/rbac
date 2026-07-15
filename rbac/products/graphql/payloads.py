import strawberry
from typing import Optional, List

from rbac.products.graphql.types import ProductType
from rbac.core.graphql.errors import MutationError


@strawberry.type
class ProductMutationPayload:
    success: bool
    product: Optional[ProductType] = None
    errors: Optional[List[MutationError]] = None

