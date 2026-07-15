from django.db import transaction
from rbac.categories.models import Category
from rbac.core.exceptions import ApplicationError, ErrorCode


@transaction.atomic
def delete_category(*, category_id):
    category = Category.objects.filter(pk=category_id).first()
    if not category:
        raise ApplicationError("Category not found.", code=ErrorCode.VALIDATION_ERROR)

    if category.children.exists():
        raise ApplicationError(
            "Cannot delete a category that has subcategories. Delete or reassign them first.",
            code=ErrorCode.BUSINESS_RULE,
        )

    category.delete()
    return True