from rbac.products.permissions import PERMISSION_REGISTRY as PRODUCTS_PERMISSIONS
from rbac.categories.permissions import PERMISSION_REGISTRY as CATEGORIES_PERMISSIONS
from rbac.orders.permissions import PERMISSION_REGISTRY as ORDERS_PERMISSIONS
# Each feature app defines its own PERMISSION_REGISTRY (codename, label, category)
# and gets aggregated here. Add a new app's import + list below as you build it.
PERMISSION_REGISTRY = [
    *PRODUCTS_PERMISSIONS,
    *CATEGORIES_PERMISSIONS,
    *ORDERS_PERMISSIONS
]       
