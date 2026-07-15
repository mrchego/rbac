from django.db import models
from rbac.core.models.base import BaseModel


class Product(BaseModel):
    company = models.ForeignKey(
        "company.Company", on_delete=models.CASCADE, related_name="products"
    )
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(fields=["company", "sku"], name="unique_product_sku_per_company")
        ]

    def __str__(self):
        return f"{self.name} ({self.sku})"