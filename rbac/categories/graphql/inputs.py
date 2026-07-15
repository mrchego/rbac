import strawberry
from typing import Optional


@strawberry.input
class CreateCategoryInput:
    name: str
    parent_id: Optional[strawberry.ID] = None


@strawberry.input
class UpdateCategoryInput:
    category_id: strawberry.ID
    name: Optional[str] = None
    parent_id: Optional[strawberry.ID] = None


@strawberry.input
class DeleteCategoryInput:
    category_id: strawberry.ID