from django.db import models
from rbac.core.models.base import BaseModel


class Category(BaseModel):
    company = models.ForeignKey(
        "company.Company", on_delete=models.CASCADE, related_name="categories"
    )
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(fields=["company", "parent", "name"], name="unique_category_name_per_parent")
        ]

    def __str__(self):
        return self.name

    @property
    def depth(self) -> int:
        """How many ancestors this category has. Root categories are depth 0."""
        depth = 0
        node = self.parent
        while node is not None:
            depth += 1
            node = node.parent
        return depth