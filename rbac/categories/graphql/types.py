import strawberry
import strawberry_django
from strawberry import auto
from typing import List, Optional

from rbac.categories.models import Category


@strawberry_django.type(Category)
class CategoryType:
    id: auto
    name: auto
    created_at: auto
    updated_at: auto

    @strawberry.field
    def parent_id(self) -> Optional[strawberry.ID]:
        return self.parent_id

    @strawberry.field
    def children(self) -> List["CategoryType"]:
        return list(self.children.all())

    @strawberry.field
    def depth(self) -> int:
        return self.depth