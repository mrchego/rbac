from django.db import models
from rbac.core.models.base import BaseModel


class UserRole(BaseModel):
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="user_roles")
    role = models.ForeignKey("authorization.Role", on_delete=models.CASCADE, related_name="user_roles")  # was "rbac.Role"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "role"], name="unique_user_role")
        ]


class UserPermissionOverride(BaseModel):
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="permission_overrides")
    permission = models.ForeignKey("authorization.Permission", on_delete=models.CASCADE)  # was "rbac.Permission"
    is_granted = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "permission"], name="unique_user_permission_override")
        ]