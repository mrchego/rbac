from django.db import models
from rbac.core.models.base import BaseModel


class Order(BaseModel):
    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        SUBMITTED = "SUBMITTED", "Submitted"
        APPROVED = "APPROVED", "Approved"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"

    company = models.ForeignKey("company.Company", on_delete=models.CASCADE, related_name="orders")
    created_by = models.ForeignKey("accounts.User", on_delete=models.SET_NULL, null=True, related_name="orders_created")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    reference = models.CharField(max_length=50)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(fields=["company", "reference"], name="unique_order_reference_per_company")
        ]

    def __str__(self):
        return f"Order {self.reference} ({self.status})"

    @property
    def total(self):
        return sum((item.quantity * item.unit_price for item in self.line_items.all()), start=0)


class OrderLineItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="line_items")
    description = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.description} x{self.quantity}"