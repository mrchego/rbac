from django.db import transaction, IntegrityError
from rbac.categories.models import Category
from rbac.core.exceptions import ApplicationError, AppValidationError, BusinessRuleViolationError, ErrorCode


def _is_descendant(candidate: Category, of: Category) -> bool:
    """True if `candidate` is `of` itself or anywhere in `of`'s subtree."""
    node = of
    while node is not None:
        if node.pk == candidate.pk:
            return True
        node = node.parent
    return False


@transaction.atomic
def update_category(*, category_id, name=None, parent_id=None):
    category = Category.objects.filter(pk=category_id).first()
    if not category:
        raise ApplicationError("Category not found.", code=ErrorCode.VALIDATION_ERROR)

    if name is not None:
        name = name.strip()
        if len(name) < 2:
            raise AppValidationError("Category name must be at least 2 characters long.", field="name")
        category.name = name

    if parent_id is not None:
        new_parent = Category.objects.filter(pk=parent_id, company=category.company).first()
        if not new_parent:
            raise ApplicationError("Parent category not found.", code=ErrorCode.VALIDATION_ERROR)
        # Prevent a category from becoming its own ancestor (a cycle).
        if _is_descendant(new_parent, of=category) or new_parent.pk == category.pk:
            raise BusinessRuleViolationError(
                "A category cannot be moved under itself or one of its own descendants.",
                code=ErrorCode.BUSINESS_RULE,
            )
        category.parent = new_parent

    try:
        category.save()
    except IntegrityError:
        raise BusinessRuleViolationError(
            "A category with this name already exists under the same parent.", code=ErrorCode.BUSINESS_RULE
        )
    return category