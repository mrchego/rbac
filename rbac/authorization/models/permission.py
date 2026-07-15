# rbac/rbac/models/permission.py
from django.db import models
from rbac.core.models.base import BaseModel


class Permission(BaseModel):
    """
    Row-per-capability, seeded from PERMISSION_REGISTRY.
    Admins never create these — they only exist to be checked off.
    """
    codename = models.CharField(max_length=100, unique=True)
    label = models.CharField(max_length=255)
    category = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ["category", "codename"]

    def __str__(self):
        return self.codename