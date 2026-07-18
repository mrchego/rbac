import strawberry
from typing import List, Optional
from decimal import Decimal


@strawberry.input
class CreateProductInput:
    name: str
    sku: str
    price: Decimal
    is_active: bool = True


@strawberry.input
class UpdateProductInput:
    product_id: strawberry.ID
    name: Optional[str] = None
    sku: Optional[str] = None
    price: Optional[Decimal] = None
    is_active: Optional[bool] = None


@strawberry.input
class DeleteProductInput:
    product_id: strawberry.ID
    
    
@strawberry.input
class ProductIdInput:
    product_id: strawberry.ID


@strawberry.input
class BulkProductIdsInput:
    product_ids: List[strawberry.ID]