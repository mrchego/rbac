from django.db import transaction, IntegrityError
from rbac.categories.models import Category
from rbac.core.exceptions import ApplicationError, AppValidationError, BusinessRuleViolationError, ErrorCode

MAX_DEPTH = 5  # arbitrary sane ceiling — adjust as you like


@transaction.atomic
def create_category(*, company, name, parent_id=None):
    name = name.strip()
    if len(name) < 2:
        raise AppValidationError("Category name must be at least 2 characters long.", field="name")

    parent = None
    if parent_id is not None:
        parent = Category.objects.filter(pk=parent_id, company=company).first()
        if not parent:
            raise ApplicationError("Parent category not found.", code=ErrorCode.VALIDATION_ERROR)
        if parent.depth + 1 >= MAX_DEPTH:
            raise BusinessRuleViolationError(
                f"Category tree cannot exceed {MAX_DEPTH} levels deep.", code=ErrorCode.BUSINESS_RULE
            )

    try:
        return Category.objects.create(company=company, name=name, parent=parent)
    except IntegrityError:
        raise BusinessRuleViolationError(
            "A category with this name already exists under the same parent.", code=ErrorCode.BUSINESS_RULE
        )