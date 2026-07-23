import strawberry
from rbac.core.exceptions import AppPermissionDeniedError
from rbac.accounts.selectors import get_current_user
from rbac.dashboard.graphql.types import DashboardData


@strawberry.type
class DashboardQuery:
    @strawberry.field
    def dashboard(self, info: strawberry.Info) -> DashboardData:
        user = get_current_user(info)
        if not user:
            raise AppPermissionDeniedError("Authentication required.")
        # Return the container unconditionally — each nested field gates itself.
        return DashboardData()