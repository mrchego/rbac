import strawberry

from rbac.products.graphql.inputs import CreateProductInput, UpdateProductInput, DeleteProductInput
from rbac.products.graphql.payloads import ProductMutationPayload
from rbac.core.graphql.payloads import SimpleMutationPayload
from rbac.products.services import create_product as create_action
from rbac.products.services import update_product as update_action
from rbac.products.services import delete_product as delete_action
from rbac.accounts.selectors import get_current_user
from rbac.authorization.decorators import require_permission
from rbac.core.exceptions import ApplicationError, AppPermissionDeniedError
from rbac.core.graphql.errors import format_application_error


@strawberry.type
class ProductMutation:
    @strawberry.mutation
    @require_permission("products.add_product")
    def create_product(self, info: strawberry.Info, input: CreateProductInput) -> ProductMutationPayload:
        current = get_current_user(info)
        if not current or not current.company_id:
            raise AppPermissionDeniedError("No company context.")
        try:
            product = create_action(
                company=current.company, name=input.name, sku=input.sku,
                price=input.price, is_active=input.is_active,
            )
            return ProductMutationPayload(success=True, product=product)
        except ApplicationError as e:
            return ProductMutationPayload(success=False, errors=[format_application_error(e)])

    @strawberry.mutation
    @require_permission("products.change_product")
    def update_product(self, info: strawberry.Info, input: UpdateProductInput) -> ProductMutationPayload:
        try:
            product = update_action(
                product_id=input.product_id, name=input.name, sku=input.sku,
                price=input.price, is_active=input.is_active,
            )
            return ProductMutationPayload(success=True, product=product)
        except ApplicationError as e:
            return ProductMutationPayload(success=False, errors=[format_application_error(e)])

    @strawberry.mutation
    @require_permission("products.delete_product")
    def delete_product(self, info: strawberry.Info, input: DeleteProductInput) -> SimpleMutationPayload:
        try:
            delete_action(product_id=input.product_id)
            return SimpleMutationPayload(success=True)
        except ApplicationError as e:
            return SimpleMutationPayload(success=False, errors=[format_application_error(e)])