import strawberry

from rbac.categories.graphql.inputs import CreateCategoryInput, UpdateCategoryInput, DeleteCategoryInput
from rbac.categories.graphql.payloads import CategoryMutationPayload
from rbac.core.graphql.payloads import SimpleMutationPayload
from rbac.categories.services import create_category as create_action
from rbac.categories.services import update_category as update_action
from rbac.categories.services import delete_category as delete_action
from rbac.accounts.selectors import get_current_user
from rbac.authorization.decorators import require_permission
from rbac.core.exceptions import ApplicationError, AppPermissionDeniedError
from rbac.core.graphql.errors import format_application_error


@strawberry.type
class CategoryMutation:
    @strawberry.mutation
    @require_permission("categories.add_category")
    def create_category(self, info: strawberry.Info, input: CreateCategoryInput) -> CategoryMutationPayload:
        current = get_current_user(info)
        if not current or not current.company_id:
            raise AppPermissionDeniedError("No company context.")
        try:
            category = create_action(company=current.company, name=input.name, parent_id=input.parent_id)
            return CategoryMutationPayload(success=True, category=category)
        except ApplicationError as e:
            return CategoryMutationPayload(success=False, errors=[format_application_error(e)])

    @strawberry.mutation
    @require_permission("categories.change_category")
    def update_category(self, info: strawberry.Info, input: UpdateCategoryInput) -> CategoryMutationPayload:
        try:
            category = update_action(category_id=input.category_id, name=input.name, parent_id=input.parent_id)
            return CategoryMutationPayload(success=True, category=category)
        except ApplicationError as e:
            return CategoryMutationPayload(success=False, errors=[format_application_error(e)])

    @strawberry.mutation
    @require_permission("categories.delete_category")
    def delete_category(self, info: strawberry.Info, input: DeleteCategoryInput) -> SimpleMutationPayload:
        try:
            delete_action(category_id=input.category_id)
            return SimpleMutationPayload(success=True)
        except ApplicationError as e:
            return SimpleMutationPayload(success=False, errors=[format_application_error(e)])