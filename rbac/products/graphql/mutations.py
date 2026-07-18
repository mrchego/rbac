import strawberry

from rbac.products.graphql.inputs import (
    CreateProductInput,
    UpdateProductInput,
    DeleteProductInput,
    ProductIdInput,
    BulkProductIdsInput,
)
from rbac.products.graphql.payloads import (
    ProductMutationPayload,
    BulkProductActionPayload,
    ProductBulkActionFailure,
)
from rbac.core.graphql.payloads import SimpleMutationPayload
from rbac.products.services import (
    create_product as create_action,
    update_product as update_action,
    delete_product as delete_action,
    activate_product as activate_action,
    deactivate_product as deactivate_action,
    bulk_activate_products,
    bulk_deactivate_products,
    bulk_delete_products,
)
from rbac.accounts.selectors import get_current_user
from rbac.authorization.decorators import require_permission
from rbac.core.exceptions import ApplicationError, AppPermissionDeniedError
from rbac.core.graphql.errors import format_application_error

def _to_bulk_payload(result) -> BulkProductActionPayload:
    return BulkProductActionPayload(
        success=len(result.failed) == 0,
        succeeded_ids=result.succeeded,
        failed=[ProductBulkActionFailure(product_id=f["product_id"], reason=f["reason"]) for f in result.failed],
    )

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
        
    @strawberry.mutation
    @require_permission("products.change_product")
    def activate_product(self, info: strawberry.Info, input: ProductIdInput) -> ProductMutationPayload:
        try:
            product = activate_action(product_id=input.product_id)
            return ProductMutationPayload(success=True, product=product)
        except ApplicationError as e:
            return ProductMutationPayload(success=False, errors=[format_application_error(e)])

    @strawberry.mutation
    @require_permission("products.change_product")
    def deactivate_product(self, info: strawberry.Info, input: ProductIdInput) -> ProductMutationPayload:
        try:
            product = deactivate_action(product_id=input.product_id)
            return ProductMutationPayload(success=True, product=product)
        except ApplicationError as e:
            return ProductMutationPayload(success=False, errors=[format_application_error(e)])

    @strawberry.mutation
    @require_permission("products.change_product")
    def bulk_activate_products(self, info: strawberry.Info, input: BulkProductIdsInput) -> BulkProductActionPayload:
        current = get_current_user(info)
        if not current or not current.company_id:
            raise AppPermissionDeniedError("No company context.")
        result = bulk_activate_products(product_ids=input.product_ids, company_id=str(current.company_id))
        return _to_bulk_payload(result)

    @strawberry.mutation
    @require_permission("products.change_product")
    def bulk_deactivate_products(self, info: strawberry.Info, input: BulkProductIdsInput) -> BulkProductActionPayload:
        current = get_current_user(info)
        if not current or not current.company_id:
            raise AppPermissionDeniedError("No company context.")
        result = bulk_deactivate_products(product_ids=input.product_ids, company_id=str(current.company_id))
        return _to_bulk_payload(result)

    @strawberry.mutation
    @require_permission("products.delete_product")
    def bulk_delete_products(self, info: strawberry.Info, input: BulkProductIdsInput) -> BulkProductActionPayload:
        current = get_current_user(info)
        if not current or not current.company_id:
            raise AppPermissionDeniedError("No company context.")
        result = bulk_delete_products(product_ids=input.product_ids, company_id=str(current.company_id))
        return _to_bulk_payload(result)