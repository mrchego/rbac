from django.db import models
from rbac.core.models.mixins import TimeStampedMixin, UUIDMixin


class BaseModel(UUIDMixin, TimeStampedMixin, models.Model):
    """
    The foundational model for the entire project.
    Ensures every model has a UUID Primary Key and Timestamps.
    """
    class Meta:
        abstract = True