# rbac/rbac/models/role.py
from django.db import models
from rbac.authorization.models.permission import Permission
from rbac.core.models.base import BaseModel


class Role(BaseModel):
    """
    A company-defined, reusable bundle of permissions.
    This is what the "Select A Role" dropdown lists.
    """
    company = models.ForeignKey(
        "company.Company", on_delete=models.CASCADE, related_name="roles"
    )
    name = models.CharField(max_length=100)
    permissions = models.ManyToManyField(
        Permission, related_name="roles", blank=True
    )
    is_default = models.BooleanField(
        default=False,
        help_text="Pre-selected for newly invited staff if no role is chosen.",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["company", "name"], name="unique_role_name_per_company"
            )
        ]
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.company.name})"