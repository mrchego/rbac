import strawberry

# accounts
from rbac.accounts.graphql.queries import UserQuery
from rbac.accounts.graphql.mutations import UserMutation

# authorization
from rbac.authorization.graphql.queries import RoleQuery
from rbac.authorization.graphql.mutations import RoleMutation

# company
from rbac.company.graphql.queries import CompanyQuery
from rbac.company.graphql.mutations import CompanyMutation

# identity
from rbac.identity.graphql.queries import SessionQuery
from rbac.identity.graphql.mutations import AuthMutation

# staff
from rbac.staff.graphql.queries import StaffQuery
from rbac.staff.graphql.mutations import StaffMutation

# products
from rbac.products.graphql.queries import ProductQuery
from rbac.products.graphql.mutations import ProductMutation

# categories
from rbac.categories.graphql.queries import CategoryQuery
from rbac.categories.graphql.mutations import CategoryMutation

# orders
from rbac.orders.graphql.queries import OrderQuery
from rbac.orders.graphql.mutations import OrderMutation


@strawberry.type
class Query(
    UserQuery,
    RoleQuery,
    CompanyQuery,
    SessionQuery,
    StaffQuery,
    ProductQuery,
    CategoryQuery,
    OrderQuery,
):
    pass


@strawberry.type
class Mutation(
    UserMutation,
    RoleMutation,
    CompanyMutation,
    AuthMutation,
    StaffMutation,
    ProductMutation,
    CategoryMutation,
    OrderMutation,
):
    pass


schema = strawberry.Schema(query=Query, mutation=Mutation)