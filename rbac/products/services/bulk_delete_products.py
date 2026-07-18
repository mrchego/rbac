from django.db import transaction
from rbac.products.selectors import get_products_by_ids
from rbac.products.services.bulk_result import BulkActionResult


@transaction.atomic
def bulk_delete_products(*, product_ids, company_id):
    """Hard-deletes matching products. If Order references Product with
    on_delete=CASCADE, this removes order history too — confirm that FK
    behavior before exposing this in a mutation; bulk_deactivate_products
    is the safer default for anything that may have been ordered."""
    result = BulkActionResult()
    product_ids = [str(pid) for pid in product_ids]
    products = list(get_products_by_ids(product_ids=product_ids, company_id=company_id))
    found_ids = {str(p.id) for p in products}

    for product in products:
        pid = str(product.id)
        product.delete()
        result.add_success(pid)

    for missing in set(product_ids) - found_ids:
        result.add_failure(missing, "Product not found in this company.")

    return result