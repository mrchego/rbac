from typing import Optional
from rbac.categories.models import Category


def get_category(*, category_id: str) -> Optional[Category]:
    return Category.objects.filter(pk=category_id).first()