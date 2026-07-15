from typing import Optional
from rbac.categories.models import Category


def list_categories(*, company_id: str, parent_id: Optional[str] = None, root_only: bool = False):
    """
    root_only=True returns only top-level categories (parent is null) — the
    natural entry point for a frontend tree view, which then lazily fetches
    each node's `.children` field as the user expands it.
    """
    qs = Category.objects.filter(company_id=company_id)
    if root_only:
        qs = qs.filter(parent__isnull=True)
    elif parent_id is not None:
        qs = qs.filter(parent_id=parent_id)
    return qs.order_by("name")