from django.core.exceptions import ValidationError

from rbac.company.models import Company

def validate_company_name(value):
    if len(value.strip()) < 2:
        raise ValidationError("Company name must be at least 2 characters long.")
    return value

def validate_company_email_unique(value, instance=None):
    qs = Company.objects.filter(email=value)
    if instance:
        qs = qs.exclude(pk=instance.pk)
    if qs.exists():
        raise ValidationError("A company with this email already exists.")
    return value