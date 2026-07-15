from django.db import models

from rbac.core.models.base import BaseModel
from rbac.core.validators.phone import validate_phone_number
from rbac.core.utils.files import (
    company_logo_light_upload_path,
    company_logo_dark_upload_path,
)


class Company(BaseModel):
    name = models.CharField(max_length=255)
    logo_light = models.ImageField(
        upload_to=company_logo_light_upload_path,
        blank=True,
        null=True,
    )

    logo_dark = models.ImageField(
        upload_to=company_logo_dark_upload_path,
        blank=True,
        null=True,
    )
    email = models.EmailField(unique=True)  # DB ensures uniqueness.
    phone = models.CharField(max_length=20, validators=[validate_phone_number])
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.TextField()
    is_active = models.BooleanField(default=True)

    # No more custom manager overriding .create()!
    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.name
