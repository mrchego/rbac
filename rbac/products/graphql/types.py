import strawberry_django
from strawberry import auto
from rbac.products.models import Product


@strawberry_django.type(Product)
class ProductType:
    id: auto
    name: auto
    sku: auto
    price: auto
    is_active: auto
    created_at: auto
    updated_at: auto